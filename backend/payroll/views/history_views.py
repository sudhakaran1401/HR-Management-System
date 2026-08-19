from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
from payroll.services.history_service import PayrollHistoryService
from payroll.forms import SalaryReportForm
from payroll.models import SalaryHistory
from payroll.services.report_service import ReportService
from payroll.services.permission_service import PermissionService

@login_required
def admin_salary_list(request):

    if not request.user.is_staff:
        return HttpResponseForbidden()

    form = SalaryReportForm(request.GET or None)

    rows = ReportService.get_filtered_salary_queryset(request).order_by("-pay_month")

    return render(
        request,
        "payroll/salary_history_admin.html",
        {
            "form": form,
            "rows": rows,
            "page_obj": rows,
            "filter_applied": any(
                [
                    request.GET.get("employee"),
                    request.GET.get("year"),
                    request.GET.get("month"),
                ]
            ),
            "show_month": True,
            "show_year": True,
            "show_employee": request.user.is_staff,
            "show_download": True,
            "reset_url": request.path,
            "csv_download_url": reverse("salary_download_csv"),
            "pdf_download_url": reverse("salary_download_pdf"),
        },
    )


@login_required
def employee_salary_history(request, employee_id=None):

    data = PayrollHistoryService.get_employee_salary_history(
        request.user, request.path, employee_id
    )

    if not data:
        return HttpResponseForbidden("Employee profile not linked.")

    return render(request, "payroll/salary_history_employee.html", data)


@login_required
def all_salary_history(request):

    if not PermissionService.is_hr_or_admin(request.user):
        return HttpResponseForbidden("Only HR/Admin can view salary history.")

    rows = SalaryHistory.objects.select_related("employee").order_by("-pay_month")

    return render(
        request,
        "payroll/all_salary_history.html",
        {
            "rows": rows,
            "page_obj": rows,
        },
    )