from django.db import transaction

from employees.models import EmployeeProfile
from employees.services.validation_service import ValidationService
from employees.services.account_service import AccountService

from employees.utils.employee_photo import clear_photo


class EmployeeService:

    @staticmethod
    def create_employee(form):

        ValidationService.validate_employee(
            form.cleaned_data.get("email"),
            form.cleaned_data.get("phone"),
        )

        with transaction.atomic():

            employee = form.save()

            AccountService.create_account(employee)

            return employee

    @staticmethod
    def update_employee(form, employee, request):

        with transaction.atomic():

            employee = (
                employee.__class__.objects
                .select_for_update()
                .get(id=employee.id)
            )

            ValidationService.validate_employee(
                form.cleaned_data.get("email"),
                form.cleaned_data.get("phone"),
                employee.id,
            )

            clear_photo(employee, request)

            return form.save()

    @staticmethod
    def get_employee_from_user(user):

        profile = (
            EmployeeProfile.objects
            .select_related("employee")
            .filter(user=user)
            .first()
        )

        if not profile:
            return None

        return profile.employee