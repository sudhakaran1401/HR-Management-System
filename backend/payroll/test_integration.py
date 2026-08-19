from decimal import Decimal
from datetime import date
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from employees.models import Employee, EmployeeProfile
from payroll.models import SalaryHistory


class PayrollAPIIntegrationTests(TestCase):
    """Integration tests for payroll API -> salary calculation -> dashboard data."""

    def setUp(self):
        self.user = User.objects.create_user(username="payroll_user", password="pass")
        self.employee = Employee.objects.create(
            name="Payroll Employee",
            email="payroll@example.com",
            department="IT",
        )
        EmployeeProfile.objects.create(user=self.user, employee=self.employee)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_payroll_then_list_and_retrieve_calculated_salary(self):
        create_response = self.client.post(
            "/api/payroll/create/",
            {
                "employee": self.employee.id,
                "pay_month": "2026-08-01",
                "amt_per_day": "1000.00",
            },
            format="json",
        )

        self.assertEqual(create_response.status_code, 201)
        salary_id = create_response.data["id"]
        salary = SalaryHistory.objects.get(pk=salary_id)
        self.assertEqual(salary.stored_net_pay, Decimal("27900.00"))

        list_response = self.client.get("/api/payroll/")
        self.assertEqual(list_response.status_code, 200)
        self.assertTrue(any(item["id"] == salary_id for item in list_response.data))

        detail_response = self.client.get(f"/api/payroll/{salary_id}/")
        self.assertEqual(detail_response.status_code, 200)
        self.assertEqual(Decimal(str(detail_response.data["stored_net_pay"])), Decimal("27900.00"))

    def test_employee_dashboard_reflects_created_payroll(self):
        SalaryHistory.objects.create(
            employee=self.employee,
            pay_month=date(2026, 8, 1),
            amt_per_day=Decimal("1000.00"),
        )

        response = self.client.get("/api/dashboard/employee/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["salary_count"], 1)
        self.assertIsNotNone(response.data["latest_salary"])
        self.assertEqual(response.data["latest_salary"]["pay_month"], "August 2026")
