from datetime import date
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
from dashboard.services.Empdashboard_service import EmployeeDashboardService
from dashboard.services.HRDashboard_service import HRDashboardService
from employees.decorators import is_admin, is_hr
from employees.models import EmployeeProfile

def _hr_or_admin(user):
    return is_admin(user) or is_hr(user)    

@login_required
def hr_dashboard(request):

    is_hr = request.user.groups.filter( name="HR" ).exists()

    if not _hr_or_admin(request.user):

        return HttpResponseForbidden( "You don't have access to this page." )

    today = date.today()

    year = request.GET.get("year")
    month = request.GET.get("month")
    day = request.GET.get("date")

    filters_applied = any([ year, month, day ])

    leave_stats = {}
    employee_stats = {}
    attendance_stats = {}
    payroll_stats = {}

    if filters_applied:

        leave_stats = HRDashboardService.get_leave_statistics( year, month, day ) 

        employee_stats = HRDashboardService.get_employee_statistics( year, month, day )

        attendance_stats = HRDashboardService.get_attendance_statistics( year, month, day ) 

        payroll_stats = HRDashboardService.get_payroll_statistics( year, month )

    return render( request, "dashboard/hr_dashboard.html",
        {

            "is_hr": is_hr,

            "total_employees": employee_stats.get( "total_employees", 0 ),

            "pending_leaves": leave_stats.get( "pending_leaves", 0 ),

            "approved_leaves": leave_stats.get( "approved_leaves", 0 ),

            "rejected_leaves": leave_stats.get( "rejected_leaves", 0 ),

            "today_attendance": attendance_stats.get( "today_attendance", 0 ),

            "present_count": attendance_stats.get( "present_count", 0 ),

            "absent_count": attendance_stats.get( "absent_count", 0 ),

            "attendance_labels": attendance_stats.get( "attendance_labels", ["Present", "Absent"] ),

            "attendance_counts": attendance_stats.get( "attendance_counts", [0, 0] ),

            "payroll_records_this_month": payroll_stats.get( "payroll_records_this_month", 0 ),

            "payroll_labels": payroll_stats.get( "payroll_labels", [] ),

            "payroll_totals": payroll_stats.get( "payroll_totals", [] ),

            "dept_labels": employee_stats.get( "dept_labels", [] ),

            "dept_counts": employee_stats.get( "dept_counts", [] ),

            "today": today,

            "years": range( 2025, today.year + 5 ),

            "months": [ (1, "Jan"), (2, "Feb"), (3, "Mar"), (4, "Apr"), (5, "May"), (6, "Jun"), 
                       (7, "Jul"), (8, "Aug"), (9, "Sep"), (10, "Oct"), (11, "Nov"), (12, "Dec") ],

            "day_range": range(1, 32),

            "hr_dashboard_url": reverse("hr_dashboard")
        }
    )


@login_required
def employee_dashboard(request):

    is_hr = request.user.groups.filter( name="HR" ).exists()

    def _employee_only(user):

        return (
            user.is_superuser or user.groups.filter( name="EMPLOYEE" ).exists() or user.groups.filter( name="HR" ).exists()
        )

    if not _employee_only(request.user):

        return HttpResponseForbidden( "You don't have access to this page." )

    profile = EmployeeProfile.objects.select_related("employee").filter(user=request.user).first()

    if not profile:

        return HttpResponseForbidden( "No EmployeeProfile linked. Contact HR." )

    emp = profile.employee

    today = date.today()

    year = request.GET.get("year")
    month = request.GET.get("month")
    day = request.GET.get("date")

    year = int(year) if year else None
    month = int(month) if month else None
    day = day if day else None

    filters_applied = any([ year, month, day ])

    attendance_data = {}
    leave_data = {}
    payroll_data = {}

    if filters_applied:

        attendance_data = EmployeeDashboardService.get_attendance_data( emp, year, month, day )

        leave_data = EmployeeDashboardService.get_leave_data( emp, year, month, day )

        payroll_data = EmployeeDashboardService .get_payroll_data( emp, year, month )

    return render( request, "dashboard/employee_dashboard.html",
        {

            "is_hr": is_hr,

            "profile": profile,

            "my_attendance_month": attendance_data.get( "my_attendance_month", 0 ),

            "attendance_month_labels": attendance_data.get( "attendance_month_labels", [] ),

            "attendance_month_data": attendance_data.get( "attendance_month_data", [] ),

            "my_approved_leaves": leave_data.get( "my_approved_leaves", [] ),

            "leave_balance": leave_data.get( "leave_balance", 0 ),

            "payroll_month_labels": payroll_data.get( "payroll_month_labels", [] ),

            "payroll_month_data": payroll_data.get( "payroll_month_data", [] ),

            "latest_salary": payroll_data.get( "latest_salary", None ),

            "salary_count": payroll_data.get( "salary_count", 0 ),

            "today": today,

            "years": range( 2025, today.year + 5 ),

            "months": [ (1, "Jan"), (2, "Feb"), (3, "Mar"), (4, "Apr"), (5, "May"), (6, "Jun"), 
                       (7, "Jul"), (8, "Aug"), (9, "Sep"), (10, "Oct"), (11, "Nov"), (12, "Dec") ],

            "day_range": range(1, 32),

            "employee_dashboard_url": reverse("employee_dashboard")
        }
    )