from django.shortcuts import render, get_object_or_404
from employees.models import Employee

def render_employee_profile( request, employee_id, viewer_role="HR" ):

    employee = get_object_or_404( Employee, id=employee_id, )

    return render( request, "employees/employee_profile.html",
        {
            "employee": employee,
            "viewer_role": viewer_role,
        },
    )

def clear_photo(employee, request):

        if request.POST.get("photo-clear"):

            if employee.photo:
                employee.photo.delete(save=False)

            employee.photo = None