from datetime import date

from django.contrib.auth.models import Group, User
from django.test import TestCase
from rest_framework.test import APIClient

from attendance.models import Attendance
from employees.models import Employee, EmployeeProfile


class AttendanceAPISecurityTests(TestCase):
    """Authorization tests for attendance APIs."""

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
        self.attendance = Attendance.objects.create(
            employee=self.other, date=date(2026, 8, 10), status="Present"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_employee_cannot_create_attendance_for_another_employee(self):
        response = self.client.post(
            "/api/attendance/create/",
            {
                "employee": self.other.id,
                "date": "2026-08-11",
                "status": "Present",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 403)

    def test_employee_cannot_update_another_employee_attendance(self):
        response = self.client.patch(
            f"/api/attendance/{self.attendance.id}/update/",
            {"status": "Absent"},
            format="json",
        )
        self.assertEqual(response.status_code, 403)

    def test_employee_cannot_delete_another_employee_attendance(self):
        response = self.client.delete(f"/api/attendance/{self.attendance.id}/delete/")
        self.assertEqual(response.status_code, 403)

    def test_employee_cannot_download_attendance_report(self):
        response = self.client.get("/api/attendance/download/csv/")
        self.assertEqual(response.status_code, 403)
