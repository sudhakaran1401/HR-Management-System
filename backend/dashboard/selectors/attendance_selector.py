from attendance.models import Attendance
from dashboard.filters.dashboard_filters import DashboardFilter


class AttendanceSelector:
    @staticmethod
    def employee_attendance(employee):

        return Attendance.objects.filter(employee=employee)

    @staticmethod
    def all_attendance():

        return Attendance.objects.all()

    @staticmethod
    def filtered_attendance(queryset, year=None, month=None, day=None):

        return DashboardFilter.apply_date_filter(queryset, "date", year, month, day)
