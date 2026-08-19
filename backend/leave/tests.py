from datetime import date

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from rest_framework.test import APIClient

from attendance.models import Attendance
from employees.models import Employee
from leave.models import LeaveBalance, LeaveRequest
from leave.services.approval_service import ApprovalService
from leave.services.balance_service import BalanceService
from leave.services.request_service import RequestService


class LeaveModelTests(TestCase):
    def setUp(self):
        self.employee = Employee.objects.create(name="John", email="john@example.com")

    def test_leave_days_are_calculated_on_save(self):
        leave = LeaveRequest.objects.create(
            employee=self.employee,
            leave_type="CASUAL",
            start_date=date(2026, 8, 10),
            end_date=date(2026, 8, 12),
        )
        self.assertEqual(leave.days, 3)
        self.assertEqual(leave.total_days, 3)

    def test_invalid_date_range_fails_model_validation(self):
        leave = LeaveRequest(
            employee=self.employee,
            start_date=date(2026, 8, 12),
            end_date=date(2026, 8, 10),
        )
        with self.assertRaises(ValidationError):
            leave.full_clean()

    def test_overlapping_leave_fails_model_validation(self):
        LeaveRequest.objects.create(
            employee=self.employee,
            start_date=date(2026, 8, 10),
            end_date=date(2026, 8, 12),
        )
        overlapping = LeaveRequest(
            employee=self.employee,
            start_date=date(2026, 8, 12),
            end_date=date(2026, 8, 14),
        )
        with self.assertRaises(ValidationError):
            overlapping.full_clean()

    def test_leave_balance_total_allowed(self):
        balance = LeaveBalance.objects.create(employee=self.employee)
        self.assertEqual(balance.total_allowed(), 50)


class LeaveServiceTests(TestCase):
    def setUp(self):
        self.employee = Employee.objects.create(name="John", email="john@example.com")

    def test_request_service_rejects_invalid_dates(self):
        leave = LeaveRequest(
            employee=self.employee,
            start_date=date(2026, 8, 12),
            end_date=date(2026, 8, 10),
        )
        valid, message = RequestService._validate_leave(self.employee, leave)
        self.assertFalse(valid)
        self.assertIn("Start date cannot be after end date", message)

    def test_request_service_rejects_attendance_conflict(self):
        Attendance.objects.create(
            employee=self.employee,
            date=date(2026, 8, 10),
            status="Present",
        )
        leave = LeaveRequest(
            employee=self.employee,
            start_date=date(2026, 8, 10),
            end_date=date(2026, 8, 11),
        )
        valid, message = RequestService._validate_leave(self.employee, leave)
        self.assertFalse(valid)
        self.assertIn("Attendance already marked as Present", message)

    def test_approval_changes_pending_leave_to_approved(self):
        leave = LeaveRequest.objects.create(
            employee=self.employee,
            start_date=date(2026, 8, 10),
            end_date=date(2026, 8, 11),
            status="PENDING",
        )
        success, message = ApprovalService.approve_leave(leave)
        leave.refresh_from_db()
        self.assertTrue(success)
        self.assertEqual(leave.status, "APPROVED")
        self.assertIn("approved", message)

    def test_non_pending_leave_cannot_be_approved_again(self):
        leave = LeaveRequest.objects.create(
            employee=self.employee,
            start_date=date(2026, 8, 10),
            end_date=date(2026, 8, 11),
            status="REJECTED",
        )
        success, message = ApprovalService.approve_leave(leave)
        self.assertFalse(success)
        self.assertIn("Only pending", message)

    def test_balance_service_counts_approved_leave_days_by_type(self):
        LeaveRequest.objects.create(
            employee=self.employee,
            leave_type="SICK",
            start_date=date(2026, 8, 1),
            end_date=date(2026, 8, 2),
            status="APPROVED",
        )
        LeaveRequest.objects.create(
            employee=self.employee,
            leave_type="CASUAL",
            start_date=date(2026, 8, 5),
            end_date=date(2026, 8, 7),
            status="PENDING",
        )
        data = BalanceService.get_leave_balance(self.employee)
        self.assertEqual(data["approved"], 1)
        self.assertEqual(data["pending"], 1)
        self.assertEqual(data["sick_applied"], 2)
        self.assertEqual(data["casual_applied"], 0)
        self.assertEqual(data["total_applied"], 2)


class LeaveAPITests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="apiuser", password="pass")
        self.employee = Employee.objects.create(name="John", email="john@example.com")
        self.client = APIClient()

    def test_leave_list_requires_authentication(self):
        response = self.client.get("/api/leave/")
        self.assertIn(response.status_code, [401, 403])

    def test_authenticated_user_can_create_leave(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/leave/create/",
            {
                "employee": self.employee.id,
                "leave_type": "CASUAL",
                "start_date": "2026-08-10",
                "end_date": "2026-08-12",
                "reason": "Personal work",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        leave = LeaveRequest.objects.get(employee=self.employee)
        self.assertEqual(leave.days, 3)
