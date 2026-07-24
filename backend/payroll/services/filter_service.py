class PayrollFilterService:

    @staticmethod
    def extract_filters(request):

        employee = request.GET.get("employee") or None

        year = request.GET.get("year") or None

        month = request.GET.get("month")

        if month in ["", None, "0"]:
            month = None

        return {
            "employee": employee,
            "year": year,
            "month": month
        }