from datetime import date
from decimal import Decimal

from django.contrib.auth.models import Group, User
from django.test import TestCase
from rest_framework.test import APIClient

from attendance.models import Attendance
from employees.models import Employee
from leave.models import LeaveRequest
from payroll.models import SalaryHistory


class HRMSSystemTests(TestCase):
    """
    System-level tests for complete HRMS workflows.

    These tests intentionally cross module boundaries instead of testing one
    model/view in isolation. They verify that the main HRMS features work
    together from authentication through employee management, attendance,
    leave approval and payroll.
    """

    def setUp(self):
        self.hr_user = User.objects.create_user(
            username="system_hr",
            password="System@12345",
        )
        hr_group, _ = Group.objects.get_or_create(name="HR")
        self.hr_user.groups.add(hr_group)
        self.hr_client = APIClient()
        self.hr_client.force_authenticate(user=self.hr_user)

        self.employee_user = User.objects.create_user(
            username="system_employee",
            password="System@12345",
        )
        employee_group, _ = Group.objects.get_or_create(name="EMPLOYEE")
        self.employee_user.groups.add(employee_group)

        self.employee = Employee.objects.create(
            name="System Test Employee",
            email="system.employee@example.com",
            phone="9999999999",
            department="IT",
            designation="Software Engineer",
            joining_date=date(2026, 1, 1),
        )
        self.employee.user = self.employee_user
        self.employee.save()

        # EmployeeProfile is created by the normal account-creation flow in
        # production. Import it here so the self-service APIs can resolve the
        # employee attached to the authenticated user.
        from employees.models import EmployeeProfile

        EmployeeProfile.objects.create(
            user=self.employee_user,
            employee=self.employee,
        )

        self.employee_client = APIClient()
        self.employee_client.force_authenticate(user=self.employee_user)

    def test_hr_complete_employee_lifecycle(self):
        """HR can complete the main employee -> attendance -> leave -> payroll flow."""
        create_response = self.hr_client.post(
            "/api/employees/create/",
            {
                "name": "Lifecycle Employee",
                "email": "lifecycle@example.com",
                "phone": "8888888888",
                "department": "IT",
                "designation": "Software Engineer",
                "joining_date": "2026-08-01",
            },
            format="json",
        )
        self.assertEqual(create_response.status_code, 201)

        employee_id = create_response.data["id"]
        lifecycle_employee = Employee.objects.get(pk=employee_id)

        attendance_response = self.hr_client.post(
            "/api/attendance/create/",
            {
                "employee": employee_id,
                "date": "2026-08-10",
                "status": "Present",
                "check_in": "09:00:00",
                "check_out": "18:00:00",
                "notes": "System test attendance",
            },
            format="json",
        )
        self.assertEqual(attendance_response.status_code, 201)
        self.assertTrue(
            Attendance.objects.filter(
                employee=lifecycle_employee,
                date=date(2026, 8, 10),
                status="Present",
            ).exists()
        )

        leave_response = self.hr_client.post(
            "/api/leave/create/",
            {
                "employee": employee_id,
                "leave_type": "CASUAL",
                "start_date": "2026-08-11",
                "end_date": "2026-08-12",
                "reason": "System test leave",
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

        leave = LeaveRequest.objects.get(pk=leave_id)
        self.assertEqual(leave.status, "APPROVED")
        self.assertEqual(leave.days, 2)

        payroll_response = self.hr_client.post(
            "/api/payroll/create/",
            {
                "employee": employee_id,
                "pay_month": "2026-08-01",
                "amt_per_day": "1000.00",
            },
            format="json",
        )
        self.assertEqual(payroll_response.status_code, 201)

        salary = SalaryHistory.objects.get(
            employee=lifecycle_employee,
            pay_month=date(2026, 8, 1),
        )
        self.assertEqual(salary.leave_taken, 2)
        self.assertEqual(salary.stored_gross, Decimal("30000.00"))
        self.assertEqual(salary.stored_net_pay, Decimal("27900.00"))

    def test_employee_self_service_workflow(self):
        """An employee can use the profile, attendance, leave and balance features."""
        profile_response = self.employee_client.get("/api/employees/me/")
        self.assertEqual(profile_response.status_code, 200)
        self.assertEqual(profile_response.data["id"], self.employee.id)

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
                "reason": "System self-service test",
            },
            format="json",
        )
        self.assertEqual(leave_response.status_code, 201)

        balance_response = self.employee_client.get(
            f"/api/leave/balance/{self.employee.id}/"
        )
        self.assertEqual(balance_response.status_code, 200)
        self.assertEqual(balance_response.data["pending"], 1)

    def test_leave_and_payroll_modules_are_integrated(self):
        """Approved leave created in the leave module is consumed by payroll."""
        leave = LeaveRequest.objects.create(
            employee=self.employee,
            leave_type="ANNUAL",
            start_date=date(2026, 8, 5),
            end_date=date(2026, 8, 9),
            status="PENDING",
        )

        approve_response = self.hr_client.post(
            f"/api/leave/{leave.id}/approve/",
            format="json",
        )
        self.assertEqual(approve_response.status_code, 200)

        payroll_response = self.hr_client.post(
            "/api/payroll/create/",
            {
                "employee": self.employee.id,
                "pay_month": "2026-08-01",
                "amt_per_day": "1200.00",
            },
            format="json",
        )
        self.assertEqual(payroll_response.status_code, 201)

        salary = SalaryHistory.objects.get(employee=self.employee)
        self.assertEqual(salary.leave_taken, 5)
        self.assertEqual(salary.stored_gross, Decimal("36000.00"))
        self.assertEqual(salary.stored_net_pay, Decimal("33480.00"))

    def test_protected_system_features_require_authentication(self):
        """Core system endpoints cannot be accessed without authentication."""
        anonymous_client = APIClient()

        protected_endpoints = [
            "/api/employees/",
            "/api/attendance/",
            "/api/leave/",
            "/api/payroll/",
            "/api/dashboard/hr/",
        ]

        for endpoint in protected_endpoints:
            with self.subTest(endpoint=endpoint):
                response = anonymous_client.get(endpoint)
                self.assertIn(response.status_code, [401, 403])
