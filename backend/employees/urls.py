from django.urls import path

from employees.views import (

    EmployeeListView,
    EmployeeCreateView,
    EmployeeDetailView,
    EmployeeUpdateView,
    EmployeeDeleteView,
    
    my_profile,
    employee_joining_report,
    employee_chart_api,
    employee_download_csv,
    employee_download_pdf,
)

urlpatterns = [

    # 👤 Employee Role

    path(
        'me/profile/',
        my_profile,
        name='my_profile'
    ),

    # 🏢 HR / Admin Role

    path(
        'hr/employees/list',
        EmployeeListView.as_view(),
        name='employee_list'
    ),

    path(
        'hr/employees/create/',
        EmployeeCreateView.as_view(),
        name='employee_create_canonical'
    ),

    path(
        'hr/employees/<int:employee_id>/',
        EmployeeDetailView.as_view(),
        name='employee_detail'
    ),

    path(
        'hr/employees/<int:employee_id>/update/',
        EmployeeUpdateView.as_view(),
        name='employee_update'
    ),

    path(
        'hr/employees/<int:employee_id>/delete/',
        EmployeeDeleteView.as_view(),
        name='employee_delete'
    ),

    path(
        "hr/employee-report/",
        employee_joining_report,
        name="employees_joining_report"
    ),

    path(
        "hr/employee-chart-api/",
        employee_chart_api,
        name="employee_chart_api"
    ),

    path(
        'hr/employees/report/csv/',
        employee_download_csv,
        name='employee_download_csv'
    ),

    path(
        'hr/employees/report/pdf/',
        employee_download_pdf,
        name='employee_download_pdf'
    ),
]