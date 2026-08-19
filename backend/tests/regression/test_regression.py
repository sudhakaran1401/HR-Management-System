from datetime import date
from decimal import Decimal

from django.contrib.auth.models import Group, User
from django.test import TestCase
from rest_framework.test import APIClient

from attendance.models import Attendance
from employees.models import Employee, EmployeeProfile
from leave.models import LeaveRequest
from payroll.models import SalaryHistory


class RegressionTests(TestCase):
    """
    Regression tests for critical HRMS functionality.
    """

    def setUp(self):
        hr_group, _ = Group.objects.get_or_create(name="HR")
        employee_group, _ = Group.objects.get_or_create(name="EMPLOYEE")

        self.hr_user = User.objects.create_user(
            username="regression_hr",
            password="Regression@12345",
        )
        self.hr_user.groups.add(hr_group)

        self.employee_user = User.objects.create_user(
            username="regression_employee",
            password="Regression@12345",
        )
        self.employee_user.groups.add(employee_group)

        self.employee = Employee.objects.create(
            user=self.employee_user,
            name="Regression Test Employee",
            email="regression.employee@example.com",
            phone="9999999999",
            department="IT",
            designation="Software Engineer",
            joining_date=date(2026, 1, 1),
        )

        EmployeeProfile.objects.create( user=self.employee_user, employee=self.employee, )

        self.hr_client = APIClient()
        self.hr_client.force_authenticate(user=self.hr_user)

        self.employee_client = APIClient()
        self.employee_client.force_authenticate(user=self.employee_user)

    def test_employee_management_regression(self):
        """Employee creation and retrieval continue to work."""

        response = self.hr_client.post(
            "/api/employees/create/",
            {
                "name": "Regression New Employee",
                "email": "regression.new@example.com",
                "phone": "8888888888",
                "department": "IT",
                "designation": "Software Engineer",
                "joining_date": "2026-08-01",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        employee_id = response.data["id"]

        detail_response = self.hr_client.get(
            f"/api/employees/{employee_id}/"
        )

        self.assertEqual(detail_response.status_code, 200)
        self.assertEqual(detail_response.data["id"], employee_id)
        self.assertEqual( detail_response.data["email"], "regression.new@example.com", )

    def test_attendance_regression(self):
        """Attendance creation remains available to authorized users."""

        response = self.hr_client.post(
            "/api/attendance/create/",
            {
                "employee": self.employee.id,
                "date": "2026-08-10",
                "status": "Present",
                "check_in": "09:00:00",
                "check_out": "18:00:00",
                "notes": "Regression attendance test",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        self.assertTrue( Attendance.objects.filter( employee=self.employee, date=date(2026, 8, 10), status="Present", ).exists() )

    def test_leave_approval_regression(self):
        """Leave approval updates status and records decision time."""

        leave = LeaveRequest.objects.create(
            employee=self.employee,
            leave_type="CASUAL",
            start_date=date(2026, 8, 18),
            end_date=date(2026, 8, 19),
            reason="Regression approval test",
        )

        response = self.hr_client.post( f"/api/leave/{leave.id}/approve/", format="json", )

        self.assertEqual(response.status_code, 200)

        leave.refresh_from_db()

        self.assertEqual(leave.status, "APPROVED")
        self.assertEqual(leave.days, 2)
        self.assertIsNotNone(leave.decided_at)

    def test_payroll_regression(self):
        """Payroll calculations continue to produce expected values."""

        response = self.hr_client.post(
            "/api/payroll/create/",
            {
                "employee": self.employee.id,
                "pay_month": "2026-08-01",
                "amt_per_day": "1000.00",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        salary = SalaryHistory.objects.get( employee=self.employee, pay_month=date(2026, 8, 1), )

        self.assertEqual(salary.worked_days, 30)
        self.assertEqual( salary.stored_gross, Decimal("30000.00"), )
        self.assertEqual( salary.stored_net_pay, Decimal("27900.00"), )

    def test_employee_self_service_regression(self):
        """Employee self-service profile and leave submission work."""

        profile_response = self.employee_client.get(
            "/api/employees/me/"
        )

        self.assertEqual(profile_response.status_code, 200)
        self.assertEqual( profile_response.data["id"], self.employee.id, )

        leave_response = self.employee_client.post(
            "/api/leave/create/",
            {
                "employee": self.employee.id,
                "leave_type": "SICK",
                "start_date": "2026-08-20",
                "end_date": "2026-08-21",
                "reason": "Regression self-service test",
            },
            format="json",
        )

        self.assertEqual(leave_response.status_code, 201)

        leave = LeaveRequest.objects.get( id=leave_response.data["id"] )

        self.assertEqual( leave.employee_id, self.employee.id, )
        self.assertEqual(leave.status, "PENDING")
        self.assertEqual(leave.days, 2)

    def test_protected_endpoints_regression(self):
        """Protected endpoints remain inaccessible anonymously."""

        anonymous_client = APIClient()

        protected_endpoints = [
            "/api/employees/",
            "/api/attendance/",
            "/api/leave/",
            "/api/payroll/",
            "/api/dashboard/hr/",
        ]

        for endpoint in protected_endpoints:
            with self.subTest(endpoint=endpoint):
                response = anonymous_client.get(endpoint)

                self.assertIn( response.status_code, [401, 403], )