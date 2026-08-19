from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.test import TestCase
from rest_framework.test import APIClient

from employees.models import Employee
from leave.models import LeaveRequest
from payroll.models import SalaryHistory


class PayrollModelTests(TestCase):
    def setUp(self):
        self.employee = Employee.objects.create(
            name="John Doe", email="john@example.com", department="IT"
        )

    def test_salary_calculates_gross_and_net_pay(self):
        salary = SalaryHistory.objects.create(
            employee=self.employee,
            pay_month=date(2026, 8, 1),
            amt_per_day=Decimal("1000.00"),
        )
        self.assertEqual(salary.basic, Decimal("21000.00"))
        self.assertEqual(salary.hra, Decimal("6000.00"))
        self.assertEqual(salary.allowances, Decimal("3000.00"))
        self.assertEqual(salary.gross, Decimal("30000.00"))
        self.assertEqual(salary.pf, Decimal("1500.00"))
        self.assertEqual(salary.tax, Decimal("600.00"))
        self.assertEqual(salary.total_deductions, Decimal("2100.00"))
        self.assertEqual(salary.net_pay, Decimal("27900.00"))
        self.assertEqual(salary.stored_net_pay, Decimal("27900.00"))
        self.assertEqual(salary.worked_days, 30)

    def test_approved_leave_is_counted_for_payroll(self):
        LeaveRequest.objects.create(
            employee=self.employee,
            leave_type="CASUAL",
            start_date=date(2026, 8, 10),
            end_date=date(2026, 8, 12),
            status="APPROVED",
        )
        salary = SalaryHistory.objects.create(
            employee=self.employee,
            pay_month=date(2026, 8, 1),
            amt_per_day=Decimal("1000.00"),
        )
        self.assertEqual(salary.leave_taken, 3)
        self.assertEqual(salary.stored_net_pay, Decimal("27900.00"))

    def test_salary_record_is_unique_per_employee_and_month(self):
        SalaryHistory.objects.create(
            employee=self.employee,
            pay_month=date(2026, 8, 1),
            amt_per_day=Decimal("1000.00"),
        )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                SalaryHistory.objects.create(
                    employee=self.employee,
                    pay_month=date(2026, 8, 1),
                    amt_per_day=Decimal("1200.00"),
                )


class PayrollAPITests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="apiuser", password="pass")
        self.employee = Employee.objects.create(name="John", email="john@example.com")
        self.client = APIClient()

    def test_payroll_list_requires_authentication(self):
        response = self.client.get("/api/payroll/")
        self.assertIn(response.status_code, [401, 403])

    def test_authenticated_user_can_create_payroll(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/payroll/create/",
            {
                "employee": self.employee.id,
                "pay_month": "2026-08-01",
                "amt_per_day": "1000.00",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        salary = SalaryHistory.objects.get(employee=self.employee)
        self.assertEqual(salary.stored_net_pay, Decimal("27900.00"))
