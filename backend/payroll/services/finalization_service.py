from django.db import transaction

class PayrollFinalizationService:

    @staticmethod
    @transaction.atomic
    def finalize_payroll(payroll):

        payroll.is_finalized = True

        payroll.save(
            update_fields=["is_finalized"]
        )

        return payroll