from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ValidationError
from employees.forms import EmployeeForm, EmployeeReportFilterForm
from employees.permissions.employee_permissions import EmployeePermission
from employees.selectors.employee_selector import EmployeeSelector
from employees.services.chart_service import ChartService
from employees.services.employee_service import EmployeeService
from employees.services.report_builder_service import EmployeeReportBuilder
from employees.services.export_service import ExportService
from employees.services.report_service import EmployeeReportService
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Employee, EmployeeProfile


class EmployeeListView(LoginRequiredMixin, ListView):

    model = Employee

    template_name = "employees/employee_list.html"

    context_object_name = "employees"

    def dispatch(self, request, *args, **kwargs):

        if not EmployeePermission.can_manage_employee(request.user):
            return HttpResponseForbidden("You don't have access.")

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):

        q = (self.request.GET.get("q") or "").strip()

        return EmployeeSelector.employee_list_query(q)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["q"] = (self.request.GET.get("q") or "").strip()

        return context
    

class EmployeeDetailView(LoginRequiredMixin, DetailView):

    model = Employee

    template_name = "employees/employee_profile.html"

    context_object_name = "employee"

    pk_url_kwarg = "employee_id"

    def dispatch(self, request, *args, **kwargs):

        if not EmployeePermission.can_view_employee(request.user):
            return HttpResponseForbidden("You don't have access.")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["viewer_role"] = "HR"

        return context

class EmployeeCreateView(LoginRequiredMixin, CreateView):

    model = Employee

    form_class = EmployeeForm

    template_name = "employees/employee_form.html"

    success_url = reverse_lazy("employee_list")

    def dispatch(self, request, *args, **kwargs):

        if not EmployeePermission.can_manage_employee(request.user):
            return HttpResponseForbidden("You don't have access.")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        try:

            self.object = EmployeeService.create_employee(form)

            return HttpResponseRedirect(
                self.get_success_url()
            )

        except ValidationError as e:

            form.add_error(None, str(e))

            return self.form_invalid(form)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["is_update"] = False

        return context


class EmployeeUpdateView(LoginRequiredMixin, UpdateView):

    model = Employee

    form_class = EmployeeForm

    template_name = "employees/employee_form.html"

    success_url = reverse_lazy("employee_list")

    pk_url_kwarg = "employee_id"

    def dispatch(self, request, *args, **kwargs):

        if not EmployeePermission.can_edit_employee(request.user):
            return HttpResponseForbidden("You don't have access.")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        try:

            EmployeeService.update_employee(
                form,
                self.get_object(),
                self.request
            )

            return super().form_valid(form)

        except ValidationError as e:

            form.add_error(None, str(e))

            return self.form_invalid(form)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["is_update"] = True

        return context
    
    
class EmployeeDeleteView(LoginRequiredMixin, DeleteView):

    model = Employee

    template_name = "employees/employee_delete.html"

    success_url = reverse_lazy("employee_list")

    pk_url_kwarg = "employee_id"

    def dispatch(self, request, *args, **kwargs):

        if not EmployeePermission.can_delete_employee(request.user):
            return HttpResponseForbidden("You don't have access.")

        return super().dispatch(request, *args, **kwargs)
    

    
@login_required
def my_profile(request):

    profile = EmployeeProfile.objects.filter(user=request.user).first()

    if not profile:
        return render(request, "employees/no_profile.html")

    return render(
        request,
        "employees/employee_profile.html",
        {
            "employee": profile.employee,
            "viewer_role": "EMPLOYEE",
        },
    )


@login_required
def employee_joining_report(request):

    if not EmployeePermission.can_view_reports(request.user):
        return HttpResponseForbidden("You don't have access.")

    form = EmployeeReportFilterForm(request.GET or None)

    month = request.GET.get("month")
    year = request.GET.get("year")

    qs = EmployeeReportService.filter_by_joining(month, year)

    filter_applied = any([month, year])

    context = {
        "form": form,
        "employees": qs,
        "filter_applied": filter_applied,
        "show_month": True,
        "show_year": True,
        "show_employee": False,
        "show_download": True,
        "reset_url": request.path,
        "csv_download_url": reverse("employee_download_csv"),
        "pdf_download_url": reverse("employee_download_pdf"),
    }

    return render( request, "employees/employees_list_report.html", context )


@login_required
def employee_chart_api(request):

    if not EmployeePermission.can_view_reports(request.user):
        return HttpResponseForbidden("You don't have access.")

    month = request.GET.get("month")
    year = request.GET.get("year")

    qs = EmployeeReportService.filter_by_joining(month, year)

    data = ChartService.get_department_chart_data(qs)

    return JsonResponse(data)


@login_required
def employee_download_csv(request):

    if not EmployeePermission.can_export_reports(request.user):
        return HttpResponseForbidden("You don't have access.")

    month = request.GET.get("month")
    year = request.GET.get("year")

    report = EmployeeReportBuilder.build_joining_report( month, year )

    return ExportService.export_csv(
        report["csv_filename"],
        report["headers"],
        report["rows"],
    )

@login_required
def employee_download_pdf(request):

    if not EmployeePermission.can_export_reports(request.user):
        return HttpResponseForbidden("You don't have access.")

    month = request.GET.get("month")
    year = request.GET.get("year")

    report = EmployeeReportBuilder.build_joining_report( month, year )

    return ExportService.export_pdf(
        report["pdf_filename"],
        month,
        year,
        report["dept_counts"],
        report["headers"],
        report["rows"],
    )