from calendar import monthrange
import calendar
import csv
from datetime import date, timedelta
from types import SimpleNamespace
from django.http import HttpResponse
from attendance.services.attendance_service import AttendanceService
from attendance.services.permission_service import AttendancePermissionService
from attendance.services.report_service import AttendanceReportService
from employees.models import Employee
from leave.models import LeaveRequest
from utils.pdf_generate import render_pdf_report

class AttendanceExportService:

    @staticmethod
    def generate_csv_response(request):
        year = request.GET.get("year")
        month = request.GET.get("month")
        employee_id = request.GET.get("employee")

        records, _ = AttendanceReportService.get_monthly_attendance_stats(
            request.user, year, month, employee_id
        )

        year = int(year) if year else date.today().year
        month = int(month) if month else None

        if month:
            start_date = date(year, month, 1)
            end_date = date(year, month, monthrange(year, month)[1])
        else:
            start_date = date(year, 1, 1)
            end_date = date(year, 12, 31)

        if AttendancePermissionService.is_hr_or_admin(request.user):
            if employee_id:
                employees = Employee.objects.filter(id=employee_id)
            else:
                employees = Employee.objects.all()
        else:
            employee = AttendanceService.get_employee_from_user(request.user)

            employees = [employee] if employee else []

        processed_records = []
        current = start_date

        while current <= end_date:
            for emp in employees:

                attendance = records.filter(employee=emp, date=current).first()

                if attendance:
                    processed_records.append(attendance)
                else:
                    leave_obj = LeaveRequest.objects.filter(
                        employee=emp,
                        status="APPROVED",
                        start_date__lte=current,
                        end_date__gte=current
                    ).first()

                    if leave_obj:
                        processed_records.append(SimpleNamespace(
                            employee=emp,
                            date=current,
                            status="Leave",
                            check_in=None,
                            check_out=None,
                            remarks=leave_obj.leave_type
                        ))

            current += timedelta(days=1)

        
        response = HttpResponse(content_type='text/csv')

        title = "Attendance Report"

        file_title = title.replace(" ", "_")

        if year:
            if month:
                month_name = calendar.month_name[int(month)]
                file_title += f"_{month_name}_{year}"
            else:
                file_title += f"_{year}"

        # Employee name (if selected)
        employee_name = None
        if employee_id:
            emp_obj = Employee.objects.filter(id=employee_id).first()
            if emp_obj:
                employee_name = emp_obj.name
                file_title += f"_{employee_name.replace(' ', '_')}"

        filename = f"{file_title}.csv"

        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        writer = csv.writer(response)

        writer.writerow([
            "Employee", "Department", "Date", "Status", "Check-in", "Check-out", "Notes"
        ])

        for r in processed_records:
            writer.writerow([
                r.employee.name,
                r.employee.department,
                r.date,
                r.status,
                r.check_in if r.check_in else "-",
                r.check_out if r.check_out else "-",
                getattr(r, "remarks", "-")
            ])

        return response
    
    @staticmethod
    def generate_pdf_response(request):
        year = request.GET.get("year")
        month = request.GET.get("month")
        employee_id = request.GET.get("employee")

        records, _ = AttendanceReportService.get_monthly_attendance_stats(
            request.user, year, month, employee_id
        )

        year = int(year) if year else date.today().year
        month = int(month) if month else None

        if month:
            start_date = date(year, month, 1)
            end_date = date(year, month, monthrange(year, month)[1])
        else:
            start_date = date(year, 1, 1)
            end_date = date(year, 12, 31)

        if AttendancePermissionService.is_hr_or_admin(request.user):
            if employee_id:
                employees = Employee.objects.filter(id=employee_id)
            else:
                employees = Employee.objects.all()
        else:
            employee = AttendanceService.get_employee_from_user(request.user)

            employees = [employee] if employee else []
        
        emp_name = None
        if employee_id:
            emp = Employee.objects.filter(id=employee_id).first()
            if emp:
                emp_name = emp.name

        processed_records = []
        current = start_date

        while current <= end_date:
            for emp in employees:

                attendance = records.filter(employee=emp, date=current).first()

                if attendance:
                    processed_records.append(attendance)
                else:
                    leave_exists = LeaveRequest.objects.filter(
                        employee=emp,
                        status="APPROVED",
                        start_date__lte=current,
                        end_date__gte=current
                    ).first()

                    if leave_exists:
                        processed_records.append(SimpleNamespace(
                            employee=emp,
                            date=current,
                            status="Leave",
                            check_in=None,
                            check_out=None,
                            remarks=leave_exists.leave_type
                        ))

            current += timedelta(days=1)

        present = 0
        leave = 0
        holiday = 0

        for r in processed_records:
            if r.status == "Present":
                present += 1
            elif r.status == "Leave":
                leave += 1
            elif r.status == "Holiday":
                holiday += 1

        headers = [
            "Employee", "Department", "Date",
            "Status", "Check-in", "Check-out", "Notes"
        ]

        rows = [
            [
                r.employee.name,
                r.employee.department,
                str(r.date),
                r.status,
                str(r.check_in) if r.check_in else "-",
                str(r.check_out) if r.check_out else "-",
                getattr(r, "remarks", "-")
            ]
            for r in processed_records
        ]
    
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="attendance_report.pdf"'

        return render_pdf_report(
            response,
            title="Attendance Report",
            summary_labels=["Present", "Leave", "Holiday"],
            summary_values=[present, leave, holiday],
            table_title="Attendance Details",
            table_headers=headers,
            table_rows=rows,
            month=month,
            year=year,
            employee_name=emp_name if emp_name else None
        )