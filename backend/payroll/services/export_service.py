import csv

from django.http import HttpResponse

from employees.models import Employee
from payroll.models import SalaryHistory
from utils.file_name import generate_filename
from utils.filters import apply_common_filters


class ExportService:
    @staticmethod
    def generate_salary_csv(request):

        qs = apply_common_filters(SalaryHistory.objects.select_related("employee"), request,"pay_month")

        response = HttpResponse(content_type='text/csv')

        title = "Payroll Report"

        year = request.GET.get("year")
        month = request.GET.get("month")
        employee_id = request.GET.get("employee")

        employee_name = None

        if employee_id:

            emp = Employee.objects.filter(id=employee_id).first()

            if emp:
                employee_name = emp.name

        filename = generate_filename(
            title,
            year,
            month,
            employee_name,
            "csv"
        )

        response['Content-Disposition'] = (f'attachment; filename="{filename}"')

        writer = csv.writer(response)

        writer.writerow([
            "Employee",
            "Department",
            "Month",
            "Gross",
            "Deduction",
            "Net Pay",
            "Paid date"
        ])

        for r in qs:

            writer.writerow([
                r.employee.name,
                r.employee.department,
                r.pay_month.strftime("%b %Y"),
                r.gross,
                r.total_deductions,
                r.net_pay,
                (
                    r.paid_date.strftime("%d-%m-%Y")
                    if r.paid_date else "-"
                )
            ])

        return response