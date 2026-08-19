from datetime import date
from decimal import Decimal

from django.contrib.auth.models import Group, User
from django.test import TestCase
from rest_framework.test import APIClient

from attendance.models import Attendance
from employees.models import Employee
from leave.models import LeaveRequest
from payroll.models import SalaryHistory


class RecoveryTests(TestCase):
    """
    Recovery tests verify that the HRMS can continue normal operations
    after an unsuccessful request or validation failure.
    """

    def setUp(self):
        hr_group, _ = Group.objects.get_or_create(name="HR")

        self.hr_user = User.objects.create_user(
            username="recovery_hr",
            password="Recovery@12345",
        )
        self.hr_user.groups.add(hr_group)

        self.employee = Employee.objects.create(
            name="Recovery Test Employee",
            email="recovery.employee@example.com",
            phone="9999999999",
            department="IT",
            designation="Software Engineer",
            joining_date=date(2026, 1, 1),
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.hr_user)

    def test_employee_creation_recovers_after_invalid_request(self):
        """A failed employee creation must not prevent a valid creation."""

        invalid_response = self.client.post(
            "/api/employees/create/",
            {
                "name": "",
                "email": "invalid",
                "phone": "",
            },
            format="json",
        )

        self.assertEqual(invalid_response.status_code, 400)

        valid_response = self.client.post(
            "/api/employees/create/",
            {
                "name": "Recovery Employee",
                "email": "recovery.new@example.com",
                "phone": "8888888888",
                "department": "IT",
                "designation": "Software Engineer",
                "joining_date": "2026-08-01",
            },
            format="json",
        )

        self.assertEqual(valid_response.status_code, 201)

        self.assertTrue(
            Employee.objects.filter(
                email="recovery.new@example.com"
            ).exists()
        )

    def test_leave_approval_recovers_after_already_approved_leave(self):
        """A failed approval of an already-approved leave must not affect a new leave."""

        approved_leave = LeaveRequest.objects.create(
            employee=self.employee,
            leave_type="CASUAL",
            start_date=date(2026, 8, 20),
            end_date=date(2026, 8, 21),
            reason="Already approved recovery test",
        )

        first_response = self.client.post(
            f"/api/leave/{approved_leave.id}/approve/",
            format="json",
        )

        self.assertEqual(first_response.status_code, 200)

        approved_leave.refresh_from_db()

        self.assertEqual(approved_leave.status, "APPROVED")
        self.assertIsNotNone(approved_leave.decided_at)

        # Try to approve the same leave again.
        failed_response = self.client.post(
            f"/api/leave/{approved_leave.id}/approve/",
            format="json",
        )

        self.assertEqual(failed_response.status_code, 400)

        # Verify the system can still process a new valid leave.
        valid_leave = LeaveRequest.objects.create(
            employee=self.employee,
            leave_type="CASUAL",
            start_date=date(2026, 8, 25),
            end_date=date(2026, 8, 26),
            reason="Valid recovery test",
        )

        valid_response = self.client.post(
            f"/api/leave/{valid_leave.id}/approve/",
            format="json",
        )

        self.assertEqual(valid_response.status_code, 200)

        valid_leave.refresh_from_db()

        self.assertEqual(valid_leave.status, "APPROVED")
        self.assertIsNotNone(valid_leave.decided_at)

    def test_attendance_recovers_after_invalid_request(self):
        """A failed attendance request must not block a valid attendance."""

        invalid_response = self.client.post(
            "/api/attendance/create/",
            {
                "employee": self.employee.id,
                "date": "invalid-date",
                "status": "InvalidStatus",
            },
            format="json",
        )

        self.assertEqual(invalid_response.status_code, 400)

        valid_response = self.client.post(
            "/api/attendance/create/",
            {
                "employee": self.employee.id,
                "date": "2026-08-15",
                "status": "Present",
                "check_in": "09:00:00",
                "check_out": "18:00:00",
                "notes": "Recovery test",
            },
            format="json",
        )

        self.assertEqual(valid_response.status_code, 201)

        self.assertTrue(
            Attendance.objects.filter(
                employee=self.employee,
                date=date(2026, 8, 15),
                status="Present",
            ).exists()
        )

    def test_payroll_recovers_after_invalid_request(self):
        """A failed payroll request must not prevent valid payroll generation."""

        invalid_response = self.client.post(
            "/api/payroll/create/",
            {
                "employee": self.employee.id,
                "pay_month": "invalid-month",
                "amt_per_day": "invalid",
            },
            format="json",
        )

        self.assertEqual(invalid_response.status_code, 400)

        valid_response = self.client.post(
            "/api/payroll/create/",
            {
                "employee": self.employee.id,
                "pay_month": "2026-08-01",
                "amt_per_day": "1000.00",
            },
            format="json",
        )

        self.assertEqual(valid_response.status_code, 201)

        salary = SalaryHistory.objects.get(
            employee=self.employee,
            pay_month=date(2026, 8, 1),
        )

        self.assertEqual(
            salary.stored_gross,
            Decimal("30000.00"),
        )