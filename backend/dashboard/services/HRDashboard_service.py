from datetime import date
from django.db.models import Count, Sum
from dashboard.selectors.attendance_selector import AttendanceSelector
from dashboard.selectors.leave_selector import LeaveSelector
from dashboard.selectors.payroll_selector import PayrollSelector
from dashboard.selectors.employee_selector import EmployeeSelector


class HRDashboardService:
    @staticmethod
    def get_leave_statistics(year=None, month=None, day=None):

        leave_base = LeaveSelector.all_leaves()

        if year:
            leave_base = leave_base.filter(applied_at__year=int(year))

        if month:
            leave_base = leave_base.filter(applied_at__icontains=f"-{int(month):02d}-")

        if day:
            leave_base = leave_base.filter(applied_at__day=int(day))

        return {
            "pending_leaves": leave_base.filter(status="PENDING").count(),
            "approved_leaves": leave_base.filter(status="APPROVED").count(),
            "rejected_leaves": leave_base.filter(status="REJECTED").count(),
        }

    @staticmethod
    def get_employee_statistics(year=None, month=None, day=None):

        employee_base = EmployeeSelector.all_employees()

        if year and month and day:
            filter_date = date(int(year), int(month), int(day))

            employee_base = employee_base.filter(joining_date__lte=filter_date)

        elif year and month:
            employee_base = employee_base.filter(
                joining_date__year=int(year), joining_date__month=int(month)
            )

        elif year:
            employee_base = employee_base.filter(joining_date__year__lte=int(year))

        total_employees = employee_base.count()

        dept_data = employee_base.values("department").annotate(count=Count("id"))

        dept_labels = [d["department"] for d in dept_data]

        dept_counts = [d["count"] for d in dept_data]

        return {
            "employee_base": employee_base,
            "total_employees": total_employees,
            "dept_labels": dept_labels,
            "dept_counts": dept_counts,
        }

    @staticmethod
    def get_attendance_statistics(year=None, month=None, day=None):

        attendance_base = AttendanceSelector.all_attendance()

        attendance_base = AttendanceSelector.filtered_attendance(
            attendance_base, year, month, day
        )

        present_count = attendance_base.filter(status="Present").count()

        absent_count = 0

        leave_range_qs = LeaveSelector.approved_leaves()

        
        if year:
            leave_range_qs = leave_range_qs.filter(start_date__year=int(year))

        if month:
            leave_range_qs = leave_range_qs.filter(start_date__month=int(month))

        if day and month and year:
            selected_date = date(int(year), int(month), int(day))

            leave_range_qs = leave_range_qs.filter( start_date__lte=selected_date, end_date__gte=selected_date )

        absent_count = sum( leave.total_days for leave in leave_range_qs )

        today_attendance = present_count + absent_count

        return {
            "today_attendance": today_attendance,
            "present_count": present_count,
            "absent_count": absent_count,
            "attendance_labels": ["Present", "Absent"],
            "attendance_counts": [present_count, absent_count],
        }

    @staticmethod
    def get_payroll_statistics(year=None, month=None):

        payroll_qs = PayrollSelector.all_payroll()

        payroll_qs = PayrollSelector.filtered_payroll(payroll_qs, year, month)

        payroll_records_this_month = payroll_qs.count()

        payroll_data = (
            payroll_qs.values("pay_month__year", "pay_month__month")
            .annotate(total=Sum("stored_net_pay"))
            .order_by("pay_month__year", "pay_month__month")
        )

        payroll_labels = []
        payroll_totals = []

        for item in payroll_data:
            y = item["pay_month__year"]
            m = item["pay_month__month"]

            payroll_labels.append(date(y, m, 1).strftime("%b %Y"))

            payroll_totals.append(float(item["total"] or 0))

        return {
            "payroll_records_this_month": payroll_records_this_month,
            "payroll_labels": payroll_labels,
            "payroll_totals": payroll_totals,
        }
