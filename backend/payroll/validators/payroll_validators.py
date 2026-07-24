from django.core.exceptions import ValidationError


class PayrollValidator:
    
    @staticmethod
    def validate_salary_values(salary):

        fields = [
            salary.basic,
            salary.hra,
            salary.allowances,
            salary.pf,
            salary.tax,
            salary.other_deductions
        ]

        for value in fields:

            if value < 0:

                raise ValidationError(
                    "Salary values cannot be negative."
                )


    @staticmethod
    def validate_payroll_editable(payroll):

        if payroll.is_finalized:
            raise ValidationError( "Finalized payroll cannot be modified." )