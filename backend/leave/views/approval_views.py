from leave.models import LeaveRequest
from leave.selectors.leave_selectors import LeaveSelector
from leave.services.approval_service import ApprovalService
from leave.constants import LeaveStatus, ViewerRole
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from leave.decorators import hr_required
from leave.utils.render import leave_request

@login_required
@hr_required
def pending_leave_requests(request, employee_id=None):

    if employee_id:

        leave_requests = ( LeaveSelector.leave_requests( employee_id=employee_id ) )

    else:

        leave_requests = ( LeaveSelector.leave_requests( status=LeaveStatus.PENDING ) )

    return render( request, "leave/my_requests.html", leave_request( leave_requests, ViewerRole.HR ), )

@login_required
@hr_required
def approve_leave(request, pk: int):

    leave = get_object_or_404(LeaveRequest, id=pk)

    ApprovalService.approve_leave(leave)

    return redirect(request.GET.get("next", "hr_all_leave_requests"))


@login_required
@hr_required
def reject_leave(request, pk: int):

    leave = get_object_or_404(LeaveRequest, id=pk)

    ApprovalService.reject_leave(leave)

    return redirect(request.GET.get("next", "hr_all_leave_requests"))


