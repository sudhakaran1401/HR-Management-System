from django.db.models import Count

class EmployeeAnalyticsService:

    @staticmethod
    def get_department_summary(qs):

        data = ( qs.values("department") .annotate(count=Count("id")) )

        result = {}

        for item in data:

            dept = item["department"] or "Unknown"

            result[dept] = item["count"]

        return result