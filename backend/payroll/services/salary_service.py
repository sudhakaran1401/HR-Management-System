from django.db import transaction
from payroll.models import SalaryHistory

from payroll.selectors.payroll_selectors import PayrollSelector
from payroll.services.calculation_service import SalaryCalculationService
from payroll.validators.payroll_validators import PayrollValidator


class SalaryService:
    @staticmethod
    def salary_exists(employee, pay_month, exclude_id=None):

        return PayrollSelector.salary_exists(employee, pay_month, exclude_id)

    @staticmethod
    def create_salary(form):

        salary = form.save(commit=False)

        SalaryService.validate_duplicate_salary(salary.employee, salary.pay_month)

        SalaryService.apply_calculation_fields(salary)

        with transaction.atomic():
            salary.save()

        return True, "Salary created successfully!"

    @staticmethod
    def update_salary(form, salary_id):

        with transaction.atomic():

            existing_salary = (
                SalaryHistory.objects
                .select_for_update()
                .get(id=salary_id)
            )

            PayrollValidator.validate_payroll_editable(
                existing_salary
            )

            salary = form.save(commit=False)

            SalaryService.validate_duplicate_salary(
                salary.employee,
                salary.pay_month,
                exclude_id=salary_id
            )

            SalaryService.apply_calculation_fields(salary)

            salary.save()

        return True, "Salary updated successfully!"

    
    @staticmethod
    def validate_duplicate_salary(employee, pay_month, exclude_id=None):

        exists = SalaryService.salary_exists(employee, pay_month, exclude_id)

        if exists:
            raise ValueError("Salary already exists.")

    @staticmethod
    def apply_calculation_fields(salary):

        result = SalaryCalculationService.calculate(
        salary.basic,
        salary.hra,
        salary.allowances,
        salary.pf,
        salary.tax,
        salary.other_deductions,
    )

        salary.stored_gross = result["gross"]

        salary.stored_total_deductions = result["total_deductions"]

        salary.stored_net_pay = result["net_pay"]

        