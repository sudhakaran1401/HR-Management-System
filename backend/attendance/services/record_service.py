from datetime import timedelta
from types import SimpleNamespace

from attendance.services.attendance_service import AttendanceService
from attendance.services.permission_service import AttendancePermissionService
from employees.models import Employee, EmployeeProfile
from leave.models import LeaveRequest


class AttendanceRecordService:

    @staticmethod
    def build_processed_records(
        user,
        records,
        start_date,
        end_date,
        employee_id=None,
    ):
        is_hr = AttendancePermissionService.is_hr_or_admin(user)

        if is_hr:
            if employee_id:
                employees = list(
                    Employee.objects.filter(id=employee_id)
                )
            else:
                employees = list(
                    Employee.objects.all()
                )

        else:
            profile = (
                EmployeeProfile.objects
                .select_related("employee")
                .filter(user=user)
                .first()
            )

            employees = (
                [profile.employee]
                if profile and profile.employee
                else []
            )

        if not employees:
            return []

        employee_ids = [emp.id for emp in employees]

        # Load attendance records once instead of querying
        # inside the employee/date loop.
        attendance_records = (
            records
            .filter(
                employee_id__in=employee_ids,
                date__range=(start_date, end_date),
            )
            .select_related("employee")
        )

        attendance_map = {
            (record.employee_id, record.date): record
            for record in attendance_records
        }

        # Load approved leave requests once.
        #
        # This preserves the original business rule:
        # start_date <= current <= end_date
        leave_requests = (
            LeaveRequest.objects
            .filter(
                employee_id__in=employee_ids,
                status="APPROVED",
                start_date__lte=end_date,
                end_date__gte=start_date,
            )
        )

        leaves_by_employee = {}

        for leave in leave_requests:
            leaves_by_employee.setdefault(
                leave.employee_id,
                []
            ).append(leave)

        processed_records = []

        current = start_date

        while current <= end_date:

            for emp in employees:

                attendance = attendance_map.get(
                    (emp.id, current)
                )

                if attendance:

                    processed_records.append(
                        SimpleNamespace(
                            employee=attendance.employee,
                            date=attendance.date,
                            status=attendance.status,
                            check_in=attendance.check_in,
                            check_out=attendance.check_out,
                            remarks=getattr(
                                attendance,
                                "remarks",
                                None,
                            ),
                        )
                    )

                else:

                    leave_obj = next(
                        (
                            leave
                            for leave in leaves_by_employee.get(
                                emp.id,
                                [],
                            )
                            if (
                                leave.start_date <= current
                                and leave.end_date >= current
                            )
                        ),
                        None,
                    )

                    if leave_obj:

                        processed_records.append(
                            SimpleNamespace(
                                employee=emp,
                                date=current,
                                status="Leave",
                                check_in=None,
                                check_out=None,
                                remarks=leave_obj.leave_type,
                            )
                        )

            current += timedelta(days=1)

        return processed_records

    @staticmethod
    def generate_processed_records(
        user,
        records,
        is_hr,
        start_date,
        end_date,
    ):

        if is_hr:

            employees = list(
                Employee.objects.all()
            )

        else:

            employee = (
                AttendanceService
                .get_employee_from_user(user)
            )

            employees = (
                [employee]
                if employee
                else []
            )

        if not employees:
            return []

        employee_ids = [emp.id for emp in employees]

        # Load attendance once.
        attendance_records = (
            records
            .filter(
                employee_id__in=employee_ids,
                date__range=(start_date, end_date),
            )
            .select_related("employee")
        )

        attendance_map = {
            (record.employee_id, record.date): record
            for record in attendance_records
        }

        # Load approved leaves once.
        leave_requests = (
            LeaveRequest.objects
            .filter(
                employee_id__in=employee_ids,
                status="APPROVED",
                start_date__lte=end_date,
                end_date__gte=start_date,
            )
        )

        leaves_by_employee = {}

        for leave in leave_requests:
            leaves_by_employee.setdefault(
                leave.employee_id,
                []
            ).append(leave)

        processed_records = []

        current = start_date

        while current <= end_date:

            for emp in employees:

                attendance = attendance_map.get(
                    (emp.id, current)
                )

                if attendance:

                    processed_records.append(
                        SimpleNamespace(
                            employee=attendance.employee,
                            date=attendance.date,
                            status=attendance.status,
                            check_in=attendance.check_in,
                            check_out=attendance.check_out,
                            notes=getattr(
                                attendance,
                                "remarks",
                                None,
                            ),
                        )
                    )

                else:

                    leave_exists = any(
                        (
                            leave.start_date <= current
                            and leave.end_date >= current
                        )
                        for leave in leaves_by_employee.get(
                            emp.id,
                            [],
                        )
                    )

                    if leave_exists:

                        processed_records.append(
                            SimpleNamespace(
                                employee=emp,
                                date=current,
                                status="Leave",
                                check_in=None,
                                check_out=None,
                                notes="On Leave",
                            )
                        )

            current += timedelta(days=1)

        return processed_records