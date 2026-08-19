from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from employees.models import Employee
from leave.constants import ViewerRole
from leave.decorators import employee_required, get_current_employee, hr_required
from leave.services.balance_service import BalanceService


@login_required
@employee_required
def my_leave_balance(request):

    employee = get_current_employee(request)

    if not employee:
        return HttpResponseForbidden("Employee profile not linked.")

    balance_data = BalanceService.get_leave_balance(employee)

    return render( request, "leave/leave_balance.html",
        {
            "employee": employee,
            "viewer_role": ViewerRole.EMPLOYEE,
            **balance_data,
        },
    )


@login_required
@hr_required
def leave_balance_by_employee(request, employee_id):

    employee = get_object_or_404( Employee, id=employee_id, )

    balance_data = BalanceService.get_leave_balance(employee)

    return render( request, "leave/leave_balance.html",
        {
            "employee": employee,
            "viewer_role": ViewerRole.HR,
            **balance_data,
        },
    )


@login_required
@employee_required
def leave_balance(request):

    employee = get_current_employee(request)

    if not employee:
        return HttpResponseForbidden("Employee profile not linked.")

    balance_data = BalanceService.get_leave_balance(employee)

    context = {"employee": employee, "viewer_role": ViewerRole.EMPLOYEE, **balance_data}

    return render(request, "leave/leave_balance.html", context)
