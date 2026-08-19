from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from employees.models import Employee, EmployeeProfile
from leave.models import LeaveRequest
from payroll.models import SalaryHistory


class ReliabilityTests(TestCase):
    """
    Reliability tests verify that repeated HRMS operations remain
    consistent and stable over multiple executions.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="reliability_user",
            password="Reliability@12345",
        )

        self.employee = Employee.objects.create(
            name="Reliability Test Employee",
            email="reliability@example.com",
            department="IT",
            designation="Software Engineer",
        )

        EmployeeProfile.objects.create(
            user=self.user,
            employee=self.employee,
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_repeated_employee_list_requests_are_consistent(self):
        """Repeated employee list requests return consistent results."""

        responses = []

        for _ in range(10):
            response = self.client.get("/api/employees/")
            self.assertEqual(response.status_code, 200)
            responses.append(response.data)

        for response_data in responses[1:]:
            self.assertEqual(response_data, responses[0])

    def test_repeated_leave_list_requests_are_consistent(self):
        """Repeated leave list requests return consistent results."""

        LeaveRequest.objects.create(
            employee=self.employee,
            leave_type="CASUAL",
            start_date=date(2026, 8, 20),
            end_date=date(2026, 8, 21),
            reason="Reliability test",
        )

        responses = []

        for _ in range(10):
            response = self.client.get("/api/leave/")
            self.assertEqual(response.status_code, 200)
            responses.append(response.data)

        for response_data in responses[1:]:
            self.assertEqual(response_data, responses[0])

    def test_repeated_payroll_reads_are_consistent(self):
        """Repeated payroll requests return the same calculated values."""

        salary = SalaryHistory.objects.create(
            employee=self.employee,
            pay_month=date(2026, 8, 1),
            amt_per_day=Decimal("1000.00"),
        )

        responses = []

        for _ in range(10):
            response = self.client.get(
                f"/api/payroll/{salary.id}/"
            )

            self.assertEqual(response.status_code, 200)
            responses.append(response.data)

        for response_data in responses[1:]:
            self.assertEqual(response_data, responses[0])

        self.assertEqual(
            Decimal(str(responses[0]["stored_net_pay"])),
            Decimal("27900.00"),
        )

    def test_repeated_leave_balance_requests_are_consistent(self):
        """Repeated leave balance requests return consistent results."""

        LeaveRequest.objects.create(
            employee=self.employee,
            leave_type="CASUAL",
            start_date=date(2026, 8, 25),
            end_date=date(2026, 8, 26),
            reason="Reliability balance test",
        )

        responses = []

        for _ in range(10):
            response = self.client.get("/api/leave/balance/")
            self.assertEqual(response.status_code, 200)
            responses.append(response.data)

        for response_data in responses[1:]:
            self.assertEqual(response_data, responses[0])

    def test_repeated_authenticated_requests_remain_available(self):
        """Authenticated API access remains available across repeated requests."""

        for _ in range(20):
            response = self.client.get("/api/me/")

            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.data["username"],
                "reliability_user",
            )