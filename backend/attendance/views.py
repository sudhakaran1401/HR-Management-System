from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from attendance.forms import MonthlyReportForm
from attendance.services.calendar_service import AttendanceCalendarService
from attendance.services.chart_service import AttendanceChartService
from attendance.services.export_service import AttendanceExportService
from employees.models import Employee
from attendance.services.permission_service import AttendancePermissionService
from attendance.services.attendance_service import AttendanceService
from attendance.services.report_service import AttendanceReportService

from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class DailyCalendarView(LoginRequiredMixin, TemplateView):
    template_name = "attendance/attendance_calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        is_hr = AttendancePermissionService.is_hr_or_admin(
            self.request.user
        )

        employees = []

        if is_hr:
            employees = Employee.objects.all().order_by("name")

        context["is_hr"] = is_hr
        context["employees"] = employees

        return context
    

class AdminAttendanceListView( LoginRequiredMixin, UserPassesTestMixin, ListView ):

    template_name = "attendance/attendance_list.html"
    context_object_name = "attendance_records"

    def test_func(self):
        return AttendancePermissionService.is_hr_or_admin(
            self.request.user
        )

    def get_queryset(self):
        return AttendanceService.get_filtered_attendance_queryset(
            self.request,
            self.request.user
        ).order_by("-date")

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["viewer_role"] = "HR"

        context["form"] = MonthlyReportForm(
            self.request.GET or None,
            is_hr=True,
            user=self.request.user
        )

        context["filter_applied"] = any([
            self.request.GET.get("year"),
            self.request.GET.get("month") not in ["", None, "0"],
            self.request.GET.get("employee")
        ])

        return context
    
class MyAttendanceView( LoginRequiredMixin, ListView ):

    template_name = "attendance/attendance_list.html"
    context_object_name = "records"

    def get_queryset(self):

        emp = AttendanceService.get_employee_from_user(
            self.request.user
        )

        if not emp:
            raise PermissionDenied(
                "Employee profile not linked."
            )

        return AttendanceService.get_employee_attendance(emp)
    
class AttendanceListView( LoginRequiredMixin, TemplateView ):

    template_name = "attendance/attendance_list.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        data = AttendanceReportService.generate_attendance_list(
            self.request
        )

        if data.get("error"):
            raise PermissionDenied(data["error"])

        context.update(data)

        return context

# @login_required
# def daily_calendar(request, employee_id=None):
#     is_hr = AttendancePermissionService.is_hr_or_admin(request.user)

#     employees = []
#     if is_hr:
#         employees = Employee.objects.all().order_by("name")

#     return render(
#         request,
#         "attendance/attendance_calendar.html",
#         {
#             "is_hr": is_hr,
#             "employees": employees,
#         },
#     )

# @login_required
# def admin_attendance_list(request):

#     if not AttendancePermissionService.is_hr_or_admin(request.user):
#         return HttpResponseForbidden("Only HR/Admin allowed.")

#     form = MonthlyReportForm(
#         request.GET or None,
#         is_hr=True,
#         user=request.user
#     )

#     rows = AttendanceService.get_filtered_attendance_queryset(request, request.user).order_by("-date")

#     context = {
#         "form": form,
#         "rows": rows,
#         "filter_applied": any([
#             request.GET.get("year"),
#             request.GET.get("month") not in ["", None, "0"],
#             request.GET.get("employee")
#         ])
#     }

#     return render(request, "attendance/admin_attendance_list.html", context)

@login_required
def mark_attendance(request, employee_id=None):

    context = AttendanceService.process_attendance_submission(request, employee_id)

    if context.get("error"):
        return HttpResponseForbidden(
            context["error"]
        )

    return render(request, "attendance/mark_attendance.html", context)

# @login_required
# def my_attendance(request):

#     emp = AttendanceService.get_employee_from_user(request.user)

#     if not emp:
#         return HttpResponseForbidden("Employee profile not linked.")

#     records = AttendanceService.get_employee_attendance(emp)

#     return render(
#         request,
#         "attendance/attendance_list.html",
#         {"records": records},
#     )

# @login_required
# def attendance_list(request):

#     data = AttendanceReportService.generate_attendance_list(request)

#     if data.get("error"):

#         return HttpResponseForbidden(data["error"])

#     return render( request, "attendance/attendance_list.html",data)

@login_required
def attendance_report(request):

    data = AttendanceReportService.generate_attendance_report(request)

    form = MonthlyReportForm(
        request.GET or None,
        is_hr=data["is_hr"],
        user=request.user
    )

    return render(request,"attendance/attendance_report.html",
        {
            "form": form,
            "records": data["records"],
            "page_obj": data["records"],
            "stats": data["stats"],
            "is_hr": data["is_hr"],
            "filter_applied": any([data["year"], data["month"], data["employee_id"]]),
            "show_month": True,
            "show_year": True,
            "show_employee": request.user.is_staff,
            "show_download": True,
            "reset_url": request.path,
            "csv_download_url": reverse("attendance_download_csv"),
            "pdf_download_url": reverse("attendance_download_pdf"),
        }
    )

@login_required
def attendance_status_chart(request):

    data = AttendanceChartService.generate_chart_data(request)

    return JsonResponse({
        "data": data
    })

@login_required
def attendance_events(request):

    employee = AttendanceService.get_employee_from_user(request.user)

    if not employee:
        return JsonResponse([], safe=False)

    events = AttendanceCalendarService.generate_employee_events(employee)

    return JsonResponse(events, safe=False)

@login_required
def attendance_download_csv(request):
    return AttendanceExportService.generate_csv_response(request)

@login_required
def attendance_download_pdf(request):

    return AttendanceExportService.generate_pdf_response(request)