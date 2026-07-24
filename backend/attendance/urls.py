from django.urls import path
from . import views

urlpatterns = [
  
    path('me/my-attendance/', views.MyAttendanceView.as_view(), name='my_attendance'),
    path('me/calendar/', views.DailyCalendarView.as_view(), name='attendance_calendar'),
    path('me/mark-attendance/', views.mark_attendance, name='mark_attendance_by_employee'),
    path('me/attendance-history/', views.AttendanceListView.as_view(), name='attendance_history'),
    path('me/monthly-report/', views.attendance_report, name='attendance_report_employee'),
    path('me/calendar/events/', views.attendance_events, name='attendance_events'),

    # 🏢 HR / Admin
    path('hr/attendance/list/', views.AdminAttendanceListView.as_view(), name='attendance_list'),
    path('hr/mark-attendance/', views.mark_attendance, name='mark_attendance'),
    path('hr/employees/<int:employee_id>/mark-attendance/', views.mark_attendance, name='mark_attendance_by_hr'),
    path('hr/attendance/monthly-report/', views.attendance_report, name='attendance_report'),
    path("hr/attendance/monthly-report/download/csv/", views.attendance_download_csv, name="attendance_download_csv"),
    path("hr/attendance/monthly-report/download/pdf/", views.attendance_download_pdf, name="attendance_download_pdf"),
    path('hr/attendance/monthly-chart/', views.attendance_status_chart, name='attendance_status_chart'),
    
]
