from payroll.models import SalaryHistory
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from payroll.services.filter_service import PayrollFilterService

class ReportService:

    def get_filtered_salary_queryset(request):
        qs = SalaryHistory.objects.all()

        filters = PayrollFilterService.extract_filters( request )
        
        employee = filters["employee"]
        year = filters["year"]
        month = filters["month"]

        if employee:
            qs = qs.filter(employee_id=employee)

        if year:
            try:
                qs = qs.filter(pay_month__year=int(year))
            except ValueError:
                pass

        if month:
            try:
                qs = qs.filter(pay_month__month=int(month))
            except ValueError:
                pass

        return qs
    
    @staticmethod
    def get_salary_chart_data(request):

        qs = ReportService.get_filtered_salary_queryset(
            request
        )

        data = (
            qs.annotate(month=TruncMonth("pay_month"))
            .values("month")
            .annotate(
                total=(
                    Sum("basic")
                    + Sum("hra")
                    + Sum("allowances")
                    - (
                        Sum("pf")
                        + Sum("tax")
                        + Sum("other_deductions")
                    )
                )
            )
            .order_by("month")
        )

        labels = [
            d["month"].strftime("%b %Y")
            for d in data
        ]

        totals = [
            float(d["total"] or 0)
            for d in data
        ]

        return {
            "labels": labels,
            "data": totals
        }
    
    @staticmethod
    def get_salary_queryset():
        return SalaryHistory.objects.select_related("employee").order_by("-pay_month")
