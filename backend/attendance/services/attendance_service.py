from attendance.forms import AttendanceForm
from attendance.models import Attendance
from attendance.services.permission_service import AttendancePermissionService
from employees.models import Employee, EmployeeProfile
from django.shortcuts import get_object_or_404
from attendance.utils import can_mark_attendance


class AttendanceService:

    @staticmethod
    def get_employee_from_user(user):

        profile = EmployeeProfile.objects.filter( user=user ).select_related("employee").first()

        return profile.employee if profile else None

    @staticmethod
    def get_employee_attendance(employee):

        return ( Attendance.objects.filter(employee=employee).order_by("-date") )

    @staticmethod
    def get_filtered_attendance_queryset(request, user):

        qs = Attendance.objects.select_related( "employee" ).all()

        year = request.GET.get("year") or None
        month = request.GET.get("month")
        employee = request.GET.get("employee") or None

        if month in ["", None, "0"]:
            month = None

        if year:
            try:
                qs = qs.filter(date__year=int(year))
            except ValueError:
                pass

        if month:
            try:
                qs = qs.filter(date__month=int(month))
            except ValueError:
                pass

        if AttendancePermissionService.is_hr_or_admin(user):

            if employee:
                qs = qs.filter(employee_id=employee)

        else:

            profile = EmployeeProfile.objects.filter( user=user ).first()

            if profile:
                qs = qs.filter(employee=profile.employee)

        return qs

    @staticmethod
    def resolve_target_employee( request, employee_id=None ):

        is_employee_mode = "/me/" in request.path

        emp = AttendanceService.get_employee_from_user(
            request.user
        )

        if not emp:
            return {
                "error": "Employee profile not linked."
            }

        if is_employee_mode:

            return {
                "employee": emp,
                "employees": None,
                "is_employee_mode": True
            }

        if request.user.is_staff:

            if employee_id:

                employee = get_object_or_404( Employee, id=employee_id )

            else:
                employee = None

            employees = Employee.objects.all()

        else:

            employee = emp
            employees = None

        return {
            "employee": employee,
            "employees": employees,
            "is_employee_mode": False
        }

    @staticmethod
    def extract_form_error(form):

        for errors in form.errors.values():

            for error in errors:
                return error

        return "Invalid form data"

    @staticmethod
    def save_or_update_attendance( attendance, employee ):
        allowed, existing_attendance = can_mark_attendance( employee, attendance.date )

        if not allowed:

            return {
                "type": "error",
                "text": (
                    f"Attendance already marked "
                    f"as {existing_attendance}"
                )
            }

        if existing_attendance:

            existing_attendance.status = attendance.status
            existing_attendance.check_in = attendance.check_in
            existing_attendance.check_out = attendance.check_out
            existing_attendance.save()

        else:

            attendance.employee = employee
            attendance.save()

        return {
            "type": "success",
            "text": "Attendance marked successfully!"
        }

    @staticmethod
    def process_attendance_submission( request, employee_id=None ):

        resolved_data = AttendanceService.resolve_target_employee( request, employee_id )
        

        if resolved_data.get("error"):
            return resolved_data

        employee = resolved_data["employee"]
        employees = resolved_data["employees"]
        is_employee_mode = resolved_data["is_employee_mode"]

        form = AttendanceForm( request.POST or None )

        message = None

        if request.method == "POST":

            if form.is_valid():

                attendance = form.save(commit=False)

                if is_employee_mode:

                    target_employee = employee

                else:

                    selected_employee_id = request.POST.get(
                        "employee"
                    )

                    target_employee = get_object_or_404( Employee, id=selected_employee_id )

                message = AttendanceService.save_or_update_attendance( attendance, target_employee )

                if message["type"] == "success":
                    form = AttendanceForm()

            else:

                message = {
                    "type": "danger",
                    "text": AttendanceService.extract_form_error(form) 
                }

        return {
            "form": form,
            "employees": employees,
            "employee": employee,
            "is_employee_mode": is_employee_mode,
            "message": message,
        }