from datetime import timedelta
from attendance.models import Attendance
from attendance.utils import can_mark_attendance
from attendance.constants import AttendanceStatus 
from django.db import transaction

class AttendanceSyncService:

    @staticmethod
    @transaction.atomic
    def sync_leave_attendance(leave):

        dates = []

        current = leave.start_date

        while current <= leave.end_date:
            dates.append(current)
            current += timedelta(days=1)

        existing_attendance = Attendance.objects.filter( employee=leave.employee, date__in=dates )

        existing_map = {
            attendance.date: attendance
            for attendance in existing_attendance
        }

        to_create = []
        to_update = []

        for date in dates:

            attendance = existing_map.get(date)

            if attendance:

                if attendance.status != AttendanceStatus.LEAVE:
                    attendance.status = AttendanceStatus.LEAVE
                    to_update.append(attendance)

            else:

                allowed, _ = can_mark_attendance( leave.employee, date )

                if allowed:

                    to_create.append( Attendance( employee=leave.employee, date=date, status=AttendanceStatus.LEAVE ) )

        if to_update:
            Attendance.objects.bulk_update( to_update, ["status"] )

        if to_create:
            Attendance.objects.bulk_create(to_create)