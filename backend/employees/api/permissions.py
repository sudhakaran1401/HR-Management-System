from rest_framework.permissions import BasePermission

from employees.decorators import is_admin, is_hr
from employees.models import EmployeeProfile


def is_hr_or_admin(user):
    return is_admin(user) or is_hr(user)


def get_current_employee(user):
    profile = (
        EmployeeProfile.objects
        .select_related("employee")
        .filter(user=user)
        .first()
    )

    if not profile:
        return None

    return profile.employee


class IsHROrAdmin(BasePermission):
    """
    Only HR users or Admin users can access the endpoint.
    """

    message = "Only HR/Admin users are allowed."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and is_hr_or_admin(request.user)
        )


class IsOwnerOrHROrAdmin(BasePermission):
    """
    HR/Admin can access everything.

    Employees can only access objects belonging to themselves.
    Supports objects containing employee_id as well as Employee objects.
    """

    message = "You do not have permission to access this record."

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        # HR/Admin can access everything
        if is_hr_or_admin(request.user):
            return True

        current_employee = get_current_employee(request.user)

        if not current_employee:
            return False

        # Attendance, LeaveRequest, SalaryHistory, etc.
        if hasattr(obj, "employee_id"):
            return obj.employee_id == current_employee.id

        # Employee object itself
        if hasattr(obj, "id") and obj.__class__.__name__ == "Employee":
            return obj.id == current_employee.id

        return False