from employees.models import Employee
from django.core.exceptions import ValidationError

class ValidationService:

    @staticmethod
    def validate_employee( email, phone, employee_id=None ):

        base_qs = Employee.objects.all()

        if employee_id:
            base_qs = base_qs.exclude( id=employee_id )

        email_exists = base_qs.filter( email=email ).exists()

        phone_exists = False

        if phone:
            phone_exists = base_qs.filter( phone=phone ).exists()

        if email_exists:
            raise ValidationError( "Email already exists." )

        if phone_exists:
            raise ValidationError( "Phone number already exists." )

        return None