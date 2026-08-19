
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from leave.constants import ViewerRole
from leave.decorators import get_current_employee, hr_required
from leave.forms import LeaveRequestForm
from leave.models import LeaveRequest
from leave.selectors.leave_selectors import LeaveSelector
from leave.services.request_service import RequestService
from leave.utils.render import leave_request
from django.shortcuts import render 
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

class LeaveListView(LoginRequiredMixin, ListView):

    model = LeaveRequest

    template_name = "leave/my_requests.html"

    context_object_name = "leave_requests"

    def get_queryset(self):

        employee = get_current_employee(self.request)

        if not employee:
            return LeaveRequest.objects.none()

        return LeaveSelector.leave_list_query(
            employee
        )
    

class LeaveCreateView(LoginRequiredMixin, CreateView):

    model = LeaveRequest

    form_class = LeaveRequestForm

    template_name = "leave/apply_leaves.html"

    success_url = reverse_lazy("my_leave_requests")
    

    def form_valid(self, form):

        employee = get_current_employee(self.request)

        if not employee:
            return HttpResponseForbidden(
                "Employee profile not linked."
            )

        try:

            RequestService.create_leave( form, employee )

            return super().form_valid(form)

        except ValidationError as e:

            form.add_error(None, str(e))

            return self.form_invalid(form)
        
class LeaveUpdateView(LoginRequiredMixin, UpdateView):

    model = LeaveRequest

    form_class = LeaveRequestForm

    template_name = "leave/apply_leaves.html"

    success_url = reverse_lazy("my_leave_requests")

    pk_url_kwarg = "leave_id"

    def form_valid(self, form):

        employee = get_current_employee(self.request)

        if not employee:
            return HttpResponseForbidden(
                "Employee profile not linked."
            )

        try:

            RequestService.update_leave(
                form,
                employee,
                self.get_object()
                
            )

            return super().form_valid(form)

        except ValidationError as e:

            form.add_error(None, str(e))

            return self.form_invalid(form)
        
class LeaveDetailView(LoginRequiredMixin, DetailView):

    model = LeaveRequest

    template_name = "leave/leave_detail.html"

    context_object_name = "leave"

    pk_url_kwarg = "leave_id"


@login_required
@hr_required
def hr_all_leave_requests(request):

    leave_requests = LeaveSelector.leave_requests()

    return render( request, "leave/leave_requests.html", leave_request( leave_requests, ViewerRole.HR, ))
