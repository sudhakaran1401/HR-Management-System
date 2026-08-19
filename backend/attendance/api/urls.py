from django.urls import path

from attendance.api.views import (
    AttendanceCalendarAPIView, 
    AttendanceCreateAPIView, 
    AttendanceDeleteAPIView,
    AttendanceDetailAPIView,
    AttendanceListAPIView,
    AttendanceReportCSVAPIView,
    AttendanceReportPDFAPIView, 
    AttendanceUpdateAPIView)

urlpatterns = [

    path('', AttendanceListAPIView.as_view()),
    path('create/', AttendanceCreateAPIView.as_view()),
    path('<int:pk>/', AttendanceDetailAPIView.as_view()),
    path('<int:pk>/update/', AttendanceUpdateAPIView.as_view()),
    path('<int:pk>/delete/', AttendanceDeleteAPIView.as_view()),
    path('calendar-events/', AttendanceCalendarAPIView.as_view()),
    path('report/', AttendanceReportCSVAPIView.as_view()),
    path('download/csv/', AttendanceReportCSVAPIView.as_view()),
    path('download/pdf/', AttendanceReportPDFAPIView.as_view()),

]