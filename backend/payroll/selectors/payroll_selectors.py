from payroll.models import SalaryHistory
from employees.models import EmployeeProfile
from django.shortcuts import get_object_or_404
from employees.models import Employee


class PayrollSelector:

    @staticmethod
    def salary_exists(employee, pay_month, exclude_id=None):

        qs = SalaryHistory.objects.filter(
            employee=employee,
            pay_month=pay_month
        )

        if exclude_id:
            qs = qs.exclude(id=exclude_id)

        return qs.exists()

    @staticmethod
    def get_salary_history(employee):

        return (
            SalaryHistory.objects
            .select_related("employee")
            .filter(employee=employee)
            .order_by("-pay_month")
        )

    @staticmethod
    def get_employee_profile(user):

        return EmployeeProfile.objects.filter(
            user=user
        ).first()

    @staticmethod
    def get_employee_by_id(employee_id):

        return get_object_or_404(
            Employee,
            id=employee_id
        )

    @staticmethod
    def get_salary_by_id(salary_id):

        return (
            SalaryHistory.objects
            .select_related("employee")
            .get(pk=salary_id)
        )

    @staticmethod
    def get_all_salary_history():

        return (
            SalaryHistory.objects
            .select_related("employee")
            .order_by("-pay_month")
        )