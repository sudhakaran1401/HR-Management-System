from payroll.models import SalaryHistory


class PayrollSelector:
    @staticmethod
    def employee_payroll(employee):

        return SalaryHistory.objects.filter(employee=employee)

    @staticmethod
    def all_payroll():

        return SalaryHistory.objects.all()

    @staticmethod
    def filtered_payroll(queryset, year=None, month=None):

        filters = {}

        if year:
            filters["pay_month__year"] = year

        if month:
            filters["pay_month__month"] = month

        return queryset.filter(**filters)
