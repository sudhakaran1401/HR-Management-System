from datetime import date

from django.contrib.auth.models import Group, User
from django.test import TestCase
from rest_framework.test import APIClient

from employees.models import Employee, EmployeeProfile
from leave.models import LeaveRequest


class LeaveAPISecurityTests(TestCase):
    """Authorization tests for leave-management APIs."""

    def setUp(self):
        self.user = User.objects.create_user(username="employee", password="pass")
        group = Group.objects.create(name="EMPLOYEE")
        self.user.groups.add(group)
        self.employee = Employee.objects.create(
            name="John Doe", email="john@example.com", department="IT"
        )
        EmployeeProfile.objects.create(user=self.user, employee=self.employee)
        self.other = Employee.objects.create(
            name="Jane Doe", email="jane@example.com", department="IT"
        )
        self.leave = LeaveRequest.objects.create(
            employee=self.other,
            leave_type="CASUAL",
            start_date=date(2026, 8, 10),
            end_date=date(2026, 8, 11),
            status="PENDING",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_employee_cannot_approve_another_employee_leave(self):
        response = self.client.post(f"/api/leave/{self.leave.id}/approve/")
        self.assertEqual(response.status_code, 403)

    def test_employee_cannot_reject_another_employee_leave(self):
        response = self.client.post(f"/api/leave/{self.leave.id}/reject/")
        self.assertEqual(response.status_code, 403)

    def test_employee_cannot_view_another_employee_leave_balance(self):
        response = self.client.get(f"/api/leave/balance/{self.other.id}/")
        self.assertEqual(response.status_code, 403)

    def test_employee_cannot_delete_another_employee_leave(self):
        response = self.client.delete(f"/api/leave/{self.leave.id}/delete/")
        self.assertEqual(response.status_code, 403)
