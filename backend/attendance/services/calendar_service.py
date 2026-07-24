from datetime import timedelta
from attendance.models import Attendance
from leave.models import LeaveRequest

class AttendanceCalendarService:

    ATTENDANCE_COLORS = {
        "Present": "#28a745",
        "Leave": "#dc3545",
        "Absent": "#007bff",
    }

    LEAVE_COLOR = "#dc3545"

    @staticmethod
    def generate_employee_events(employee):

        attendance_records = Attendance.objects.filter( employee=employee )

        leave_records = LeaveRequest.objects.filter( employee=employee, status="APPROVED" )

        date_map = {}

        # Attendance Events
        for record in attendance_records:

            date_str = record.date.strftime("%Y-%m-%d")

            color = AttendanceCalendarService.ATTENDANCE_COLORS.get(
                record.status,
                "#007bff"
            )

            date_map[date_str] = {
                "title": f"{employee.name} - {record.status}",
                "start": date_str,
                "color": color
            }

        # Leave Events
        for leave in leave_records:

            current = leave.start_date

            while current <= leave.end_date:

                date_str = current.strftime("%Y-%m-%d")

                date_map[date_str] = {
                    "title": f"{employee.name} - {leave.leave_type}",
                    "start": date_str,
                    "color": AttendanceCalendarService.LEAVE_COLOR
                }

                current += timedelta(days=1)

        return list(date_map.values())