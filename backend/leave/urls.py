from django.urls import path

from leave.views import (

    # Employee
    LeaveListView,
    LeaveCreateView,
    LeaveUpdateView,

    leave_balance,
    my_leave_balance,

    # HR/Admin
    approve_leave,
    reject_leave,
    pending_leave_requests,
    leave_balance_by_employee,
    hr_all_leave_requests,

    # Reports
    leave_report,
    leave_report_download_csv,
    leave_report_download_pdf,
)

urlpatterns = [

    # 👤 Employee

    path(
        'me/apply/',
        LeaveCreateView.as_view(),
        name='apply_leave'
    ),

    path(
        'me/update/<int:leave_id>/',
        LeaveUpdateView.as_view(),
        name='update_leave'
    ),

    path(
        'me/my-requests/',
        LeaveListView.as_view(),
        name='my_leave_requests'
    ),

    path(
        'me/balance/',
        leave_balance,
        name='leave_balance'
    ),

    path(
        'me/leave-balance/',
        my_leave_balance,
        name='my_leave_balance'
    ),

    # 🏢 HR / Admin

    path(
        'hr/approve/<int:pk>/',
        approve_leave,
        name='approve_leave'
    ),

    path(
        'hr/reject/<int:pk>/',
        reject_leave,
        name='reject_leave'
    ),

    path(
        'hr/employees/<int:employee_id>/leave-requests/',
        pending_leave_requests,
        name='hr_employee_leave_requests'
    ),

    path(
        'hr/employees/<int:employee_id>/leave-balance/',
        leave_balance_by_employee,
        name='leave_balance_by_employee'
    ),

    path(
        'hr/all-leave-requests/',
        hr_all_leave_requests,
        name='hr_all_leave_requests'
    ),

    # 📊 Reports

    path(
        'hr/leave-report/',
        leave_report,
        name='leave_report'
    ),

    path(
        "hr/leave-report/download/csv/",
        leave_report_download_csv,
        name="leave_report_download_csv"
    ),

    path(
        "hr/leave-report/download/pdf/",
        leave_report_download_pdf,
        name="leave_report_download_pdf"
    ),
]