from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from datetime import date

from employees.models import Employee, EmployeeProfile
from leave.models import LeaveRequest


class LeaveAPIIntegrationTests(TestCase):
    """Integration tests for leave creation -> approval -> balance."""

    def setUp(self):
        self.user = User.objects.create_user(username="leave_user", password="pass")
        self.employee = Employee.objects.create(
            name="Leave Employee",
            email="leave@example.com",
            department="IT",
        )
        EmployeeProfile.objects.create(user=self.user, employee=self.employee)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_leave_then_approve_and_verify_balance(self):
        create_response = self.client.post(
            "/api/leave/create/",
            {
                "employee": self.employee.id,
                "leave_type": "CASUAL",
                "start_date": "2026-08-12",
                "end_date": "2026-08-14",
                "reason": "Personal work",
            },
            format="json",
        )

        self.assertEqual(create_response.status_code, 201)
        leave_id = create_response.data["id"]
        leave = LeaveRequest.objects.get(pk=leave_id)
        self.assertEqual(leave.days, 3)
        self.assertEqual(leave.status, "PENDING")

        approve_response = self.client.post(f"/api/leave/{leave_id}/approve/")
        self.assertEqual(approve_response.status_code, 200)

        leave.refresh_from_db()
        self.assertEqual(leave.status, "APPROVED")

        balance_response = self.client.get("/api/leave/balance/")
        self.assertEqual(balance_response.status_code, 200)
        self.assertEqual(balance_response.data["casual_applied"], 3)
        self.assertEqual(balance_response.data["total_applied"], 3)

    def test_leave_list_reflects_created_request(self):
        leave = LeaveRequest.objects.create(
            employee=self.employee,
            leave_type="SICK",
            start_date=date(2026, 8, 20),
            end_date=date(2026, 8, 21),
            reason="Medical appointment",
    )

        response = self.client.get("/api/leave/")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(any(item["id"] == leave.id for item in response.data))
