from datetime import timedelta
from types import SimpleNamespace
from attendance.services.attendance_service import AttendanceService
from attendance.services.permission_service import AttendancePermissionService
from employees.models import Employee, EmployeeProfile
from leave.models import LeaveRequest


class AttendanceRecordService:

    @staticmethod
    def build_processed_records(user, records, start_date, end_date,employee_id=None):

        is_hr = AttendancePermissionService.is_hr_or_admin(user)

        if is_hr:

            if employee_id:
                employees = Employee.objects.filter(id=employee_id)
            else:
                employees = Employee.objects.all()

        else:

            profile = EmployeeProfile.objects.filter(user=user).first()

            employees = [profile.employee] if profile else []

        processed_records = []

        current = start_date

        while current <= end_date:

            for emp in employees:

                attendance = records.filter( employee=emp, date=current ).first()

                if attendance:

                    processed_records.append(
                        SimpleNamespace(
                            employee=attendance.employee,
                            date=attendance.date,
                            status=attendance.status,
                            check_in=attendance.check_in,
                            check_out=attendance.check_out,
                            remarks=getattr( attendance, "remarks", None )
                        )
                    )

                else:

                    leave_obj = LeaveRequest.objects.filter(
                        employee=emp,
                        status="APPROVED",
                        start_date__lte=current,
                        end_date__gte=current
                    ).first()

                    if leave_obj:

                        processed_records.append(
                            SimpleNamespace(
                                employee=emp,
                                date=current,
                                status="Leave",
                                check_in=None,
                                check_out=None,
                                remarks=leave_obj.leave_type
                            )
                        )

            current += timedelta(days=1)

        return processed_records
    
    @staticmethod
    def generate_processed_records(user, records, is_hr, start_date, end_date):

        if is_hr:
            employees = Employee.objects.all()
        else:
            employee = AttendanceService.get_employee_from_user(user)
            employees = [employee] if employee else []

        processed_records = []
        current = start_date

        while current <= end_date:
            for emp in employees:

                attendance = records.filter(employee=emp, date=current).first()

                if attendance:
                    processed_records.append(SimpleNamespace(
                        employee=attendance.employee,
                        date=attendance.date,
                        status=attendance.status,
                        check_in=attendance.check_in,
                        check_out=attendance.check_out,
                        notes=getattr(attendance, "remarks", None)
                    ))
                else:
                    leave_exists = LeaveRequest.objects.filter(
                        employee=emp,
                        status="APPROVED",
                        start_date__lte=current,
                        end_date__gte=current
                    ).exists()

                    if leave_exists:
                        processed_records.append(SimpleNamespace(
                            employee=emp,
                            date=current,
                            status="Leave",
                            check_in=None,
                            check_out=None,
                            notes="On Leave"
                        ))
                    else:
                        continue  

            current += timedelta(days=1)

        return processed_records