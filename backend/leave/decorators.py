from django.http import HttpResponseForbidden
from functools import wraps

from employees.models import EmployeeProfile
from leave.services.permission_service import  PermissionService 

def employee_required(view_func):

    def wrapper(request, *args, **kwargs):

        allowed = request.user.is_superuser or request.user.groups.filter( name__in=["EMPLOYEE", "HR", "ADMIN"] ).exists()

        if not allowed:
            return HttpResponseForbidden( "You don't have access to this page." )

        return view_func(request, *args, **kwargs)

    return wrapper

def hr_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not PermissionService.hr_or_admin( request.user ):

            return HttpResponseForbidden( "Only HR/Admin allowed." )

        return view_func( request, *args, **kwargs )

    return wrapper

def get_employee_or_forbidden(user):

    profile = ( EmployeeProfile.objects .select_related("employee") .filter(user=user) .first() )

    if not profile or not profile.employee:

        return None

    return profile.employee

def get_current_employee(request):

    profile = EmployeeProfile.objects.select_related("employee").filter(user=request.user).first()

    if not profile or not profile.employee:
        return None

    return profile.employee