from django.db.models import Count, Sum
from dashboard.utils.date_filters import DashboardDateFilter
from leave.models import LeaveBalance

from dashboard.selectors.attendance_selector import AttendanceSelector
from dashboard.selectors.leave_selector import LeaveSelector
from dashboard.selectors.payroll_selector import PayrollSelector
from dashboard.utils.chart_formatter import ChartFormatter


class EmployeeDashboardService:
    @staticmethod
    def get_attendance_data(emp, year=None, month=None, day=None):

        attendance_base = AttendanceSelector.employee_attendance(emp)

        attendance_base = AttendanceSelector.filtered_attendance(
            attendance_base, year, month, day
        )

        attendance_qs = attendance_base.filter(status="Present")

        month_labels = []
        worked_days_data = []

        my_attendance_month = 0

        if year and not month:
            monthly_data = attendance_qs.values("date__month").annotate(
                total=Count("id")
            )

            attendance_dict = {
                item["date__month"]: item["total"] for item in monthly_data
            }

            my_attendance_month = sum(attendance_dict.values())

            month_labels, worked_days_data = ChartFormatter.monthly_chart(
                attendance_dict, year
            )

        elif month:
            month_count = attendance_qs.count()

            my_attendance_month = month_count

            month_labels, worked_days_data = ChartFormatter.single_month_chart(
                month, month_count
            )

        else:
            count = attendance_qs.count()

            my_attendance_month = count

            month_labels = ["Filtered"]

            worked_days_data = [count]

        return {
            "my_attendance_month": my_attendance_month,
            "attendance_month_labels": month_labels,
            "attendance_month_data": worked_days_data,
        }

    @staticmethod
    def get_leave_data(emp, year=None, month=None, day=None):

        balance = LeaveBalance.objects.get_or_create(employee=emp)[0]

        approved_leaves = LeaveSelector.approved_employee_leaves(emp)

        approved_leaves = DashboardDateFilter.apply_filters( approved_leaves, "start_date", year, month, )

        if day and "-" in str(day):
            approved_leaves = approved_leaves.filter(start_date=day)

        total_approved_days = sum(leave.total_days for leave in approved_leaves)

        total_allowed = balance.sick_leave + balance.casual_leave + balance.annual_leave

        leave_balance = total_allowed - total_approved_days

        return {
            "my_approved_leaves": approved_leaves,
            "leave_balance": leave_balance,
        }

    @staticmethod
    def get_payroll_data(emp, year=None, month=None):

        payroll_qs = PayrollSelector.employee_payroll(emp)

        payroll_qs = PayrollSelector.filtered_payroll(payroll_qs, year, month)

        payroll_values = payroll_qs.values("pay_month__month").annotate(
            total=Sum("stored_net_pay")
        )

        payroll_dict = {
            item["pay_month__month"]: float(item["total"] or 0)
            for item in payroll_values
        }

        payroll_month_labels = []
        payroll_month_data = []

        salary_count = 0
        latest_salary = payroll_qs.order_by("-pay_month").first()

        if year and not month:
            payroll_month_labels, payroll_month_data = ChartFormatter.monthly_chart(
                payroll_dict, year
            )

            salary_count = sum(1 for value in payroll_dict.values() if value > 0)

        elif month:
            value = payroll_dict.get(int(month), 0)

            payroll_month_labels, payroll_month_data = (
                ChartFormatter.single_month_chart(month, value)
            )

            salary_count = 1 if value else 0

            
        else:

            salary_count = payroll_qs.count()

            payroll_month_labels = ["Payroll"]

            payroll_month_data = [
                float(latest_salary.stored_net_pay)
            ] if latest_salary else []  
       

        return {
            "payroll_month_labels": payroll_month_labels,
            "payroll_month_data": payroll_month_data,
            "salary_count": salary_count,
            "latest_salary": latest_salary,
        }
