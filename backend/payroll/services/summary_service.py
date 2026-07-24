from django.db.models import Sum

class PayrollSummaryService:

    @staticmethod
    def get_summary(qs):

        total_payrolls = qs.count()

        total_net_pay = (
            qs.aggregate(
                total=Sum("stored_net_pay")
            )["total"] or 0
        )

        return {
            "total_payrolls": total_payrolls,
            "total_net_pay": total_net_pay
        }