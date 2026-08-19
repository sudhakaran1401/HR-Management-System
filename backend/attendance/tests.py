from datetime import date, time

from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.test import TestCase
from rest_framework.test import APIClient

from attendance.models import Attendance
from attendance.services.attendance_service import AttendanceService
from employees.models import Employee, EmployeeProfile


class AttendanceModelTests(TestCase):
    def setUp(self):
        self.employee = Employee.objects.create(
            name="John Doe", email="john@example.com", department="IT"
        )

    def test_attendance_string_representation(self):
        attendance = Attendance.objects.create(
            employee=self.employee, date=date(2026, 8, 1), status="Present"
        )
        self.assertEqual(str(attendance), "John Doe (IT) | 2026-08-01 | Present")

    def test_same_employee_cannot_have_two_records_on_same_date(self):
        Attendance.objects.create(
            employee=self.employee, date=date(2026, 8, 1), status="Present"
        )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Attendance.objects.create(
                    employee=self.employee, date=date(2026, 8, 1), status="Leave"
                )


class AttendanceServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="employee", password="pass")
        self.employee = Employee.objects.create(
            name="John Doe", email="john@example.com", department="IT"
        )
        EmployeeProfile.objects.create(user=self.user, employee=self.employee)

    def test_get_employee_from_user_returns_linked_employee(self):
        self.assertEqual(AttendanceService.get_employee_from_user(self.user), self.employee)

    def test_get_employee_attendance_returns_latest_first(self):
        Attendance.objects.create(employee=self.employee, date=date(2026, 8, 1))
        Attendance.objects.create(employee=self.employee, date=date(2026, 8, 3))
        records = list(AttendanceService.get_employee_attendance(self.employee))
        self.assertEqual(records[0].date, date(2026, 8, 3))

    def test_save_or_update_attendance_creates_first_record(self):
        attendance = Attendance(
            date=date(2026, 8, 5),
            status="Present",
            check_in=time(9, 0),
            check_out=time(17, 0),
        )
        result = AttendanceService.save_or_update_attendance(attendance, self.employee)
        self.assertEqual(result["type"], "success")
        self.assertTrue(Attendance.objects.filter(employee=self.employee, date=date(2026, 8, 5)).exists())

    def test_save_or_update_attendance_blocks_existing_marked_record(self):
        Attendance.objects.create(
            employee=self.employee, date=date(2026, 8, 5), status="Present"
        )
        attendance = Attendance(date=date(2026, 8, 5), status="Leave")
        result = AttendanceService.save_or_update_attendance(attendance, self.employee)
        self.assertEqual(result["type"], "error")
        self.assertIn("Attendance already marked", result["text"])


class AttendanceAPITests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="apiuser", password="pass")
        self.employee = Employee.objects.create(name="John", email="john@example.com")
        self.client = APIClient()

    def test_attendance_list_requires_authentication(self):
        response = self.client.get("/api/attendance/")
        self.assertIn(response.status_code, [401, 403])

    def test_authenticated_user_can_create_attendance(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "employee": self.employee.id,
            "date": "2026-08-05",
            "status": "Present",
            "check_in": "09:00:00",
            "check_out": "17:00:00",
            "notes": "On time",
        }
        response = self.client.post("/api/attendance/create/", payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Attendance.objects.count(), 1)
