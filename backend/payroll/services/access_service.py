from employees.models import Employee
from payroll.selectors.payroll_selectors import PayrollSelector
from django.shortcuts import get_object_or_404

class PayrollAccessService:
    @staticmethod
    def get_target_employee(user, path, employee_id=None):

        profile = PayrollSelector.get_employee_profile(user)

        if not profile:
            return None

        employee = profile.employee

        is_employee_mode = "/me/" in path

        if is_employee_mode:
            return employee

        if user.is_staff:
            return get_object_or_404(Employee, id=employee_id)

        return employee
