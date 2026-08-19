from datetime import date
from decimal import Decimal

from django.contrib.auth.models import Group, User
from django.test import TestCase
from rest_framework.test import APIClient

from attendance.models import Attendance
from dashboard.services.Empdashboard_service import EmployeeDashboardService
from dashboard.services.HRDashboard_service import HRDashboardService
from employees.models import Employee, EmployeeProfile
from leave.models import LeaveRequest
from payroll.models import SalaryHistory


class DashboardServiceTests(TestCase):
    def setUp(self):
        self.employee = Employee.objects.create(
            name="John Doe",
            email="john@example.com",
            department="IT",
            joining_date=date(2026, 1, 10),
        )

    def test_hr_employee_statistics_counts_employees(self):
        Employee.objects.create(name="Jane", email="jane@example.com", department="HR")
        data = HRDashboardService.get_employee_statistics()
        self.assertEqual(data["total_employees"], 2)
        self.assertCountEqual(data["dept_labels"], ["IT", "HR"])

    def test_hr_attendance_statistics_counts_present_records(self):
        Attendance.objects.create(
            employee=self.employee, date=date(2026, 8, 10), status="Present"
        )
        data = HRDashboardService.get_attendance_statistics("2026", "8", "10")
        self.assertEqual(data["present_count"], 1)
        self.assertEqual(data["today_attendance"], 1)

    def test_employee_dashboard_attendance_counts_present_days(self):
        Attendance.objects.create(
            employee=self.employee, date=date(2026, 8, 1), status="Present"
        )
        Attendance.objects.create(
            employee=self.employee, date=date(2026, 8, 2), status="Present"
        )
        data = EmployeeDashboardService.get_attendance_data(self.employee, 2026, 8)
        self.assertEqual(data["my_attendance_month"], 2)

    def test_employee_dashboard_leave_balance_reflects_approved_days(self):
        LeaveRequest.objects.create(
            employee=self.employee,
            start_date=date(2026, 8, 10),
            end_date=date(2026, 8, 12),
            status="APPROVED",
        )
        data = EmployeeDashboardService.get_leave_data(self.employee, 2026, 8)
        self.assertEqual(data["leave_balance"], 47)

    def test_employee_dashboard_returns_latest_payroll(self):
        SalaryHistory.objects.create(
            employee=self.employee,
            pay_month=date(2026, 8, 1),
            amt_per_day=Decimal("1000.00"),
        )
        data = EmployeeDashboardService.get_payroll_data(self.employee, 2026, 8)
        self.assertEqual(data["salary_count"], 1)
        self.assertEqual(data["latest_salary"].pay_month, date(2026, 8, 1))


class DashboardAPITests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="employee", password="pass")
        self.hr_user = User.objects.create_user(username="hr", password="pass")
        hr_group = Group.objects.create(name="HR")
        self.hr_user.groups.add(hr_group)

        self.employee = Employee.objects.create(
            name="John Doe", email="employee@example.com", department="IT"
        )
        EmployeeProfile.objects.create(user=self.user, employee=self.employee)
        self.client = APIClient()

    def test_employee_dashboard_requires_authentication(self):
        response = self.client.get("/api/dashboard/employee/")
        self.assertIn(response.status_code, [401, 403])

    def test_employee_dashboard_returns_data_for_linked_employee(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/dashboard/employee/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("leave_balance", response.data)
        self.assertIn("salary_count", response.data)

    def test_hr_dashboard_rejects_regular_employee(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/dashboard/hr/")
        self.assertEqual(response.status_code, 403)

    def test_hr_dashboard_allows_hr_user(self):
        self.client.force_authenticate(user=self.hr_user)
        response = self.client.get("/api/dashboard/hr/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("total_employees", response.data)
