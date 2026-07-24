from django.urls import path

from employees.api.views import (
 EmployeeCreateAPIView,
 EmployeeDeleteAPIView,
 EmployeeDetailAPIView,
 EmployeeListAPIView,
 EmployeeReportCSVAPIView,
 EmployeeReportPDFAPIView, 
 EmployeeUpdateAPIView,
 MyProfileAPIView
 )


urlpatterns = [
    path("me/", MyProfileAPIView.as_view()),
    path('', EmployeeListAPIView.as_view()),
    path('create/', EmployeeCreateAPIView.as_view()),
    path('<int:pk>/', EmployeeDetailAPIView.as_view()),
    path('<int:pk>/update/', EmployeeUpdateAPIView.as_view()),
    path('<int:pk>/delete/', EmployeeDeleteAPIView.as_view()),
    path('download/csv', EmployeeReportCSVAPIView.as_view()),
    path('download/pdf', EmployeeReportPDFAPIView.as_view()),
]