from datetime import date
from decimal import Decimal

from django.contrib.auth.models import Group, User
from django.test import TestCase
from rest_framework.test import APIClient

from employees.models import Employee, EmployeeProfile
from payroll.models import SalaryHistory


class PayrollAPISecurityTests(TestCase):
    """Authorization tests for payroll APIs."""

    def setUp(self):
        self.user = User.objects.create_user(username="employee", password="pass")
        group = Group.objects.create(name="EMPLOYEE")
        self.user.groups.add(group)

        self.employee = Employee.objects.create(
            name="John Doe", email="john@example.com", department="IT"
        )
        EmployeeProfile.objects.create(
            user=self.user, employee=self.employee
        )

        self.other = Employee.objects.create(
            name="Jane Doe", email="jane@example.com", department="IT"
        )

        # Another employee's payroll — used for authorization tests.
        self.salary = SalaryHistory.objects.create(
            employee=self.other,
            pay_month=date(2026, 8, 1),
            amt_per_day=Decimal("1000.00"),
        )

        # Logged-in employee's own payroll — used for list visibility test.
        self.my_salary = SalaryHistory.objects.create(
            employee=self.employee,
            pay_month=date(2026, 9, 1),
            amt_per_day=Decimal("1200.00"),
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_employee_can_list_only_own_payroll_records(self):
        response = self.client.get("/api/payroll/")

        self.assertEqual(response.status_code, 200)

        data = response.json()
        records = (
            data["results"]
            if isinstance(data, dict) and "results" in data
            else data
        )

        self.assertGreater(len(records), 0)

        for record in records:
            self.assertEqual(record["employee"], self.employee.id)

    def test_employee_cannot_create_payroll(self):
        response = self.client.post(
            "/api/payroll/create/",
            {
                "employee": self.other.id,
                "pay_month": "2026-09-01",
                "amt_per_day": "1000.00",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 403)

    def test_employee_cannot_update_payroll(self):
        response = self.client.patch(
            f"/api/payroll/{self.salary.id}/update/",
            {"amt_per_day": "2000.00"},
            format="json",
        )
        self.assertEqual(response.status_code, 403)

    def test_employee_cannot_delete_payroll(self):
        response = self.client.delete(
            f"/api/payroll/{self.salary.id}/delete/"
        )
        self.assertEqual(response.status_code, 403)

    def test_employee_cannot_download_another_employee_payslip(self):
        response = self.client.get(
            f"/api/payroll/{self.salary.id}/payslip/"
        )
        self.assertEqual(response.status_code, 403)