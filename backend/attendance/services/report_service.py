import calendar
from calendar import monthrange
from collections import Counter
from datetime import date, timedelta
from types import SimpleNamespace
from attendance.models import Attendance
from attendance.services.attendance_service import AttendanceService
from attendance.services.permission_service import AttendancePermissionService
from attendance.services.record_service import AttendanceRecordService
from employees.models import Employee
from leave.models import LeaveRequest

class AttendanceReportService:

    @staticmethod
    def get_monthly_attendance_stats(user, year=None, month=None, employee_id=None):

        qs = Attendance.objects.all()

        if year:
            try:
                qs = qs.filter(date__year=int(year))
            except ValueError:
                pass

        if month:
            try:
                qs = qs.filter(date__month=int(month))
            except ValueError:
                pass

        employee = None

        # HR/Admin
        if AttendancePermissionService.is_hr_or_admin(user):
            if employee_id:
                qs = qs.filter(employee_id=employee_id)
                employee = Employee.objects.filter(id=employee_id).first()

        else:
            employee = AttendanceService.get_employee_from_user(user)

            if employee:
                qs = qs.filter(employee=employee)

        present = qs.filter(status="Present").count()
        holiday = qs.filter(status="Holiday").count()

        leave_days = 0

        if employee and year and month:
            year = int(year)
            month = int(month)

            month_start = date(year, month, 1)
            month_end = date(year, month, monthrange(year, month)[1])

            leaves = LeaveRequest.objects.filter(
                employee=employee,
                status="APPROVED",
                start_date__lte=month_end,
                end_date__gte=month_start
            )

            for leave in leaves:
                start = max(leave.start_date, month_start)
                end = min(leave.end_date, month_end)
                leave_days += (end - start).days + 1

        stats = {
            "Present": present,
            "Leave": leave_days,
            "Holiday": holiday
        }

        return qs, stats

    @staticmethod
    def generate_attendance_report(request):

        user = request.user
        is_hr = AttendancePermissionService.is_hr_or_admin(user)

        year = request.GET.get("year")
        month = request.GET.get("month")
        employee_id = request.GET.get("employee")

        records, _ = AttendanceReportService.get_monthly_attendance_stats(user, year, month, employee_id)

        processed_records = []
        
        if year or month:

            year = int(year) if year else date.today().year
            month = int(month) if month else None

            # Date range
            if month:

                start_date = date(year, month, 1)
                end_date = date(year, month, calendar.monthrange(year, month)[1])

            else:

                start_date = date(year, 1, 1)
                end_date = date(year, 12, 31)

            processed_records = (
                AttendanceRecordService.build_processed_records(
                    user=user,
                    records=records,
                    start_date=start_date,
                    end_date=end_date,
                    employee_id=employee_id
                )
            )

        counter = Counter(
            [r.status for r in processed_records]
        )

        stats = {
            "Present": counter.get("Present", 0),
            "Leave": counter.get("Leave", 0),
            "Holiday": counter.get("Holiday", 0),
        }

        return {
            "records": processed_records,
            "stats": stats,
            "year": year,
            "month": month,
            "employee_id": employee_id,
            "is_hr": is_hr
        }

    
    
    @staticmethod
    def generate_attendance_list(request):

        is_employee_mode = "/me/" in request.path

        emp = AttendanceService.get_employee_from_user(
            request.user
        )

        if not emp:
            return {
                "error": "Employee profile not linked."
            }

        if is_employee_mode:

            records = Attendance.objects .select_related("employee") .filter(employee=emp) .order_by("date") 

            employees = [emp]

        else:

            if ( AttendancePermissionService.is_hr_or_admin(request.user) ):

                records = Attendance.objects.select_related("employee").all().order_by("date")

                employees = Employee.objects.all()

            else:

                records = Attendance.objects.select_related("employee").filter(employee=emp).order_by("date")

                employees = [emp]

        final_records = []

        if records.exists():

            start_date = records.first().date
            end_date = records.last().date

            current = start_date

            while current <= end_date:

                for employee in employees:

                    attendance = records.filter( employee=employee, date=current ).first()

                    if attendance:

                        final_records.append(
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

                        leave = (
                            LeaveRequest.objects.filter(
                                employee=employee,
                                status="APPROVED",
                                start_date__lte=current,
                                end_date__gte=current
                            ).first()
                        )

                        if leave:

                            final_records.append(
                                SimpleNamespace(
                                    employee=employee,
                                    date=current,
                                    status="Leave",
                                    check_in=None,
                                    check_out=None,
                                    remarks=( f"{leave.leave_type} " f"LEAVE" )
                                )
                            )

                current += timedelta(days=1)

        final_records = final_records[::-1]

        viewer_role = ( "HR" if ( not is_employee_mode and AttendancePermissionService.is_hr_or_admin(request.user) ) else "EMP" )

        return {
            "attendance_records": final_records,
            "page_obj": final_records,
            "viewer_role": viewer_role,
        }