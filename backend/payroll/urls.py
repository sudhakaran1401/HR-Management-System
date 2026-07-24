from django.urls import path
from . import views

urlpatterns = [
    # 👤 Employee
    path( "me/salary-list/", views.employee_salary_history, name="employee_salary_history" ),
    path("me/payslip/<int:employee_id>/", views.payslip_pdf, name="payslip_pdf"),
    path( "me/payslip/<int:employee_id>/pay-details/", views.PayslipDetailView.as_view(), name="payslip_view", ),
    # 🏢 HR/Admin
    path( "hr/salary-update/<int:pk>/", views.SalaryUpdateView.as_view(), name="update_salary", ),
    path( "hr/payslip/<int:employee_id>/pay-details/", views.PayslipDetailView.as_view(), name="hr_payslip_view", ),
    path("hr/salary-create/", views.SalaryCreateView.as_view(), name="create_salary"),
    path("hr/salary-history/", views.all_salary_history, name="all_salary_history"),
    path( "hr/salary-list/", views.AdminSalaryListView.as_view(), name="admin_salary_list" ),
    path("hr/salary-chart/", views.salary_chart_api, name="salary_chart_api"),
    path( "hr/employees/<int:employee_id>/salary-history/", views.employee_salary_history, name="employee_salary_history_hr", ),
    path( "hr/salary-list/download/csv/", views.salary_download_csv, name="salary_download_csv", ),
    path( "hr/salary-list/download/pdf/", views.salary_download_pdf, name="salary_download_pdf", ),
]
