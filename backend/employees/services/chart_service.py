from employees.services.analytics_service import EmployeeAnalyticsService

class ChartService:

    @staticmethod
    def get_department_chart_data(qs):

        summary = EmployeeAnalyticsService.get_department_summary(qs)

        return {
            "labels": list(summary.keys()),
            "data": list(summary.values()),
        }