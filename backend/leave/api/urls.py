from django.urls import path
from leave.api.views import (
    LeaveApproveAPIView, 
    LeaveBalanceAPIView, 
    LeaveRejectAPIView,
    LeaveReportAPIView,
    LeaveReportCSVAPIView,
    LeaveReportPDFAPIView, 
    LeaveRequestCreateAPIView, 
    LeaveRequestDeleteAPIView, 
    LeaveRequestDetailAPIView, 
    LeaveRequestListAPIView, 
    LeaveRequestUpdateAPIView
)

urlpatterns = [

    path('', LeaveRequestListAPIView.as_view()),
    path('create/', LeaveRequestCreateAPIView.as_view()),
    path('<int:pk>/', LeaveRequestDetailAPIView.as_view()),
    path('<int:pk>/update/', LeaveRequestUpdateAPIView.as_view()),
    path('<int:pk>/delete/', LeaveRequestDeleteAPIView.as_view()),
    path('balance/', LeaveBalanceAPIView.as_view()),
    path('balance/<int:employee_id>/', LeaveBalanceAPIView.as_view()),
    path("<int:pk>/approve/", LeaveApproveAPIView.as_view()),
    path("<int:pk>/reject/", LeaveRejectAPIView.as_view()),
    path("report/", LeaveReportAPIView.as_view()),
    path("download/csv/", LeaveReportCSVAPIView.as_view()),
    path("download/pdf/", LeaveReportPDFAPIView.as_view()),

]