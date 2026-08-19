from datetime import date
from decimal import Decimal

from django.contrib.auth.models import Group, User
from django.test import TestCase
from rest_framework.test import APIClient

from attendance.models import Attendance
from employees.models import Employee, EmployeeProfile
from leave.models import LeaveRequest
from payroll.models import SalaryHistory


class AcceptanceTests(TestCase):
    """
    Acceptance tests based on the main HRMS business requirements.

    These tests verify that a real HR user or employee can complete the
    expected business task successfully from the API level.
    """

    def setUp(self):
        hr_group, _ = Group.objects.get_or_create(name="HR")
        employee_group, _ = Group.objects.get_or_create(name="EMPLOYEE")

        self.hr_user = User.objects.create_user(
            username="acceptance_hr",
            password="Acceptance@12345",
        )
        self.hr_user.groups.add(hr_group)

        self.employee_user = User.objects.create_user(
            username="acceptance_employee",
            password="Acceptance@12345",
        )
        self.employee_user.groups.add(employee_group)

        self.employee = Employee.objects.create(
            name="Acceptance Test Employee",
            email="acceptance.employee@example.com",
            phone="9999999999",
            department="IT",
            designation="Software Engineer",
            joining_date=date(2026, 1, 1),
        )
        EmployeeProfile.objects.create(
            user=self.employee_user,
            employee=self.employee,
        )

        self.hr_client = APIClient()
        self.hr_client.force_authenticate(user=self.hr_user)

        self.employee_client = APIClient()
        self.employee_client.force_authenticate(user=self.employee_user)

    def test_hr_acceptance_employee_management(self):
        """HR can add an employee and the employee appears in the HR list."""
        response = self.hr_client.post(
            "/api/employees/create/",
            {
                "name": "Accepted New Employee",
                "email": "accepted.new@example.com",
                "phone": "8888888888",
                "department": "IT",
                "designation": "Software Engineer",
                "joining_date": "2026-08-01",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        employee_id = response.data["id"]

        list_response = self.hr_client.get("/api/employees/")
        self.assertEqual(list_response.status_code, 200)
        self.assertTrue(
            any(item["id"] == employee_id for item in list_response.data)
        )

    def test_employee_acceptance_attendance_and_leave(self):
        """An employee can view attendance and successfully submit leave."""
        attendance = Attendance.objects.create(
            employee=self.employee,
            date=date(2026, 8, 13),
            status="Present",
        )

        attendance_response = self.employee_client.get("/api/attendance/")
        self.assertEqual(attendance_response.status_code, 200)
        self.assertTrue(
            any(item["id"] == attendance.id for item in attendance_response.data)
        )

        leave_response = self.employee_client.post(
            "/api/leave/create/",
            {
                "employee": self.employee.id,
                "leave_type": "SICK",
                "start_date": "2026-08-20",
                "end_date": "2026-08-21",
                "reason": "Acceptance test leave",
            },
            format="json",
        )

        self.assertEqual(leave_response.status_code, 201)
        leave = LeaveRequest.objects.get(id=leave_response.data["id"])
        self.assertEqual(leave.status, "PENDING")
        self.assertEqual(leave.days, 2)

    def test_hr_acceptance_leave_approval(self):
        """HR can approve a valid employee leave request."""
        leave = LeaveRequest.objects.create(
            employee=self.employee,
            leave_type="CASUAL",
            start_date=date(2026, 8, 18),
            end_date=date(2026, 8, 19),
            reason="Acceptance approval test",
        )

        response = self.hr_client.post(
            f"/api/leave/{leave.id}/approve/",
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        leave.refresh_from_db()
        self.assertEqual(leave.status, "APPROVED")
        self.assertEqual(leave.days, 2)
        self.assertIsNotNone(leave.decided_at)

    def test_hr_acceptance_payroll_generation(self):
        """HR can generate a monthly payslip with the expected salary result."""
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

        salary = SalaryHistory.objects.get(
            employee=self.employee,
            pay_month=date(2026, 8, 1),
        )
        self.assertEqual(salary.stored_gross, Decimal("30000.00"))
        self.assertEqual(salary.stored_net_pay, Decimal("27900.00"))
        self.assertEqual(salary.worked_days, 30)

    def test_acceptance_complete_employee_business_flow(self):
        """An accepted HRMS flow works from employee leave to approved payroll."""
        leave_response = self.employee_client.post(
            "/api/leave/create/",
            {
                "employee": self.employee.id,
                "leave_type": "ANNUAL",
                "start_date": "2026-08-05",
                "end_date": "2026-08-06",
                "reason": "Complete acceptance flow",
            },
            format="json",
        )
        self.assertEqual(leave_response.status_code, 201)
        leave_id = leave_response.data["id"]

        approve_response = self.hr_client.post(
            f"/api/leave/{leave_id}/approve/",
            format="json",
        )
        self.assertEqual(approve_response.status_code, 200)

        payroll_response = self.hr_client.post(
            "/api/payroll/create/",
            {
                "employee": self.employee.id,
                "pay_month": "2026-08-01",
                "amt_per_day": "1000.00",
            },
            format="json",
        )
        self.assertEqual(payroll_response.status_code, 201)

        salary = SalaryHistory.objects.get(employee=self.employee)
        self.assertEqual(salary.leave_taken, 2)
        self.assertEqual(salary.stored_gross, Decimal("30000.00"))
        self.assertEqual(salary.stored_net_pay, Decimal("27900.00"))