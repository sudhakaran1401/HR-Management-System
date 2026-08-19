from django.urls import path


from dashboard.api.views import EmployeeDashboardAPIView, HRDashboardAPIView

urlpatterns = [

    path( "employee/", EmployeeDashboardAPIView.as_view(), name="employee-dashboard-api"),
    path( "hr/", HRDashboardAPIView.as_view(), name="employee-dashboard-api")


]