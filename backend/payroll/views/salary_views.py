from django.http import HttpResponseForbidden
from payroll.forms import SalaryForm, SalaryReportForm
from payroll.models import SalaryHistory
from payroll.services.report_service import ReportService
from payroll.services.salary_service import SalaryService
from payroll.services.permission_service import PermissionService
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.urls import reverse_lazy


class AdminSalaryListView(LoginRequiredMixin, ListView):

    model = SalaryHistory

    template_name = "payroll/salary_history_admin.html"

    context_object_name = "rows"

    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_staff:
            return HttpResponseForbidden()

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):

        return (
            ReportService
            .get_filtered_salary_queryset(self.request)
            .order_by("-pay_month")
        )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        form = SalaryReportForm(self.request.GET or None)

        context.update({
            "form": form,
            "filter_applied": any([
                self.request.GET.get("employee"),
                self.request.GET.get("year"),
                self.request.GET.get("month"),
            ]),
            "show_month": True,
            "show_year": True,
            "show_employee": self.request.user.is_staff,
            "show_download": True,
            "reset_url": self.request.path,
            "csv_download_url": reverse("salary_download_csv"),
            "pdf_download_url": reverse("salary_download_pdf"),
        })

        return context
    
class SalaryCreateView(LoginRequiredMixin, CreateView):

    model = SalaryHistory

    form_class = SalaryForm

    template_name = "payroll/create_salary.html"

    success_url = reverse_lazy("all_salary_history")

    def dispatch(self, request, *args, **kwargs):

        if not PermissionService.is_hr_or_admin(request.user):
            return HttpResponseForbidden(
                "Only HR/Admin can create payroll records."
            )

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        success, text = SalaryService.create_salary(form)

        if not success:

            form.add_error(None, text)

            return self.form_invalid(form)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["is_update"] = False

        return context
    

class SalaryUpdateView(LoginRequiredMixin, UpdateView):

    model = SalaryHistory

    form_class = SalaryForm

    template_name = "payroll/create_salary.html"

    success_url = reverse_lazy("all_salary_history")

    pk_url_kwarg = "pk"

    def dispatch(self, request, *args, **kwargs):

        if not PermissionService.is_hr_or_admin(request.user):
            return HttpResponseForbidden()

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        success, text = SalaryService.update_salary(
            form,
            self.get_object().id
        )

        if not success:

            form.add_error(None, text)

            return self.form_invalid(form)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["is_update"] = True

        return context

class PayslipDetailView(LoginRequiredMixin, DetailView):

    model = SalaryHistory

    template_name = "payroll/payslip_view.html"

    context_object_name = "salary"

    pk_url_kwarg = "employee_id"

    queryset = SalaryHistory.objects.select_related("employee")