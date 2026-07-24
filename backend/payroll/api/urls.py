from django.urls import path

from payroll.api.views import (
    PayrollCSVDownloadAPIView,
    PayrollCreateAPIView, 
    PayrollDeleteAPIView, 
    PayrollDetailAPIView, 
    PayrollListAPIView,
    PayrollPDFDownloadAPIView, 
    PayrollUpdateAPIView, 
    PayslipDownloadAPIView)

urlpatterns = [

    path('', PayrollListAPIView.as_view()),
    path('create/', PayrollCreateAPIView.as_view()),
    path('<int:pk>/', PayrollDetailAPIView.as_view()),
    path('<int:pk>/update/', PayrollUpdateAPIView.as_view()),
    path('<int:pk>/delete/', PayrollDeleteAPIView.as_view()),
    path('<int:pk>/payslip/', PayslipDownloadAPIView.as_view()),
    path('download/csv/', PayrollCSVDownloadAPIView.as_view()),
    path('download/pdf/', PayrollPDFDownloadAPIView.as_view()),

]