from datetime import date

from django.contrib.auth.models import Group, User
from django.test import TestCase
from rest_framework.test import APIClient

from employees.models import Employee, EmployeeProfile


class EmployeeAPISecurityTests(TestCase):
    """Authorization tests for employee-management APIs."""

    def setUp(self):
        self.user = User.objects.create_user(username="employee", password="pass")
        self.employee_group = Group.objects.create(name="EMPLOYEE")
        self.user.groups.add(self.employee_group)
        self.employee = Employee.objects.create(
            name="John Doe",
            email="john@example.com",
            department="IT",
            designation="Software Engineer",
            joining_date=date(2026, 8, 1),
        )
        EmployeeProfile.objects.create(user=self.user, employee=self.employee)
        self.other = Employee.objects.create(
            name="Jane Doe",
            email="jane@example.com",
            department="HR",
            designation="HR Manager",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_employee_cannot_list_all_employees(self):
        response = self.client.get("/api/employees/")
        self.assertEqual(response.status_code, 403)

    def test_employee_cannot_create_employee(self):
        response = self.client.post(
            "/api/employees/create/",
            {
                "name": "New Person",
                "email": "new@example.com",
                "department": "IT",
                "designation": "Software Engineer",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 403)

    def test_employee_cannot_update_another_employee(self):
        response = self.client.patch(
            f"/api/employees/{self.other.id}/update/",
            {"name": "Tampered Name"},
            format="json",
        )
        self.assertEqual(response.status_code, 403)

    def test_employee_cannot_delete_another_employee(self):
        response = self.client.delete(f"/api/employees/{self.other.id}/delete/")
        self.assertEqual(response.status_code, 403)
