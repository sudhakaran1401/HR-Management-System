from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render
from leave.services.export_service import ExportService
from leave.decorators import hr_required
from leave.forms import LeaveReportFilterForm
from leave.models import LeaveRequest
from leave.services.leave_report_builder import LeaveReportBuilder

def get_leave_report(request):

    return LeaveReportBuilder.build(
        month=request.GET.get("month"),
        year=request.GET.get("year"),
        employee_id=request.GET.get("employee"),
    )


@login_required
@hr_required
def leave_report(request):

    form = LeaveReportFilterForm(
        request.GET or None
    )

    report = {
        "queryset": LeaveRequest.objects.none(),
        "summary": {
            "total": 0,
            "approved": 0,
            "pending": 0,
            "rejected": 0,
        },
    }

    filter_applied = False

    if form.is_valid():

        month = form.cleaned_data.get("month")

        year = form.cleaned_data.get("year")

        employee = form.cleaned_data.get(
            "employee"
        )

        report = LeaveReportBuilder.build(
            month=month,
            year=year,
            employee_id=(
                employee.id
                if employee
                else None
            ),
        )

        filter_applied = any([
            month,
            year,
            employee,
        ])

    context = {
        "form": form,
        "leave_requests": report["queryset"],
        "is_hr": True,
        "filter_applied": filter_applied,
        "total": report["summary"]["total"],
        "approved": report["summary"]["approved"],
        "pending": report["summary"]["pending"],
        "rejected": report["summary"]["rejected"],
        "show_month": True,
        "show_year": True,
        "show_employee": request.user.is_staff,
        "show_download": True,
        "reset_url": request.path,
        "csv_download_url": reverse(
            "leave_report_download_csv"
        ),
        "pdf_download_url": reverse(
            "leave_report_download_pdf"
        ),
    }

    return render(
        request,
        "leave/leave_report.html",
        context,
    )


@login_required
@hr_required
def leave_report_download_csv(request):

    report = get_leave_report(request)

    return ExportService.export_csv(
        report["csv_filename"],
        report["headers"],
        report["rows"],
    )


@login_required
@hr_required
def leave_report_download_pdf(request):

    report = get_leave_report(request)

    return ExportService.export_pdf(
        report["pdf_filename"],
        request.GET.get("month"),
        request.GET.get("year"),
        report["employee_name"],
        report["summary"],
        report["headers"],
        report["rows"],
    )