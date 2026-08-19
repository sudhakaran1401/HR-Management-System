from datetime import date

from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.db import IntegrityError, transaction
from rest_framework.test import APIClient

from employees.models import Employee, EmployeeProfile
from employees.permissions.employee_permissions import EmployeePermission
from employees.services.account_service import AccountService


class EmployeeModelTests(TestCase):
    def test_employee_string_representation(self):
        employee = Employee.objects.create(
            name="John Doe",
            email="john@example.com",
            department="IT",
            designation="Software Engineer",
        )
        self.assertEqual(str(employee), "John Doe (IT)")

    def test_employee_email_is_unique(self):
        Employee.objects.create(name="John", email="john@example.com")
        duplicate = Employee(name="Jane", email="john@example.com")
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                duplicate.save()


class AccountServiceTests(TestCase):
    def test_generate_username_adds_suffix_for_duplicate(self):
        User.objects.create_user(username="john", email="old@example.com")
        username = AccountService.generate_username("john@example.com")
        self.assertEqual(username, "john1")

    def test_generate_password_uses_first_name(self):
        employee = Employee(name="john doe", email="john@example.com")
        self.assertEqual(AccountService.generate_password(employee), "John@123")

    def test_create_account_links_profile_and_assigns_employee_group(self):
        employee = Employee.objects.create(
            name="John Doe",
            email="john@example.com",
            department="IT",
        )

        user = AccountService.create_account(employee)

        self.assertEqual(user.username, "john")
        self.assertTrue(user.check_password("John@123"))
        self.assertEqual(employee.user, user)
        self.assertTrue(EmployeeProfile.objects.filter(user=user, employee=employee).exists())
        self.assertTrue(user.groups.filter(name="EMPLOYEE").exists())
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_hr_account_gets_hr_group_and_staff_access(self):
        employee = Employee.objects.create(
            name="Helen HR",
            email="helen@example.com",
            department="HR",
        )
        user = AccountService.create_account(employee)

        self.assertTrue(user.groups.filter(name="HR").exists())
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)


class EmployeePermissionTests(TestCase):
    def test_hr_can_manage_employees(self):
        user = User.objects.create_user(username="hr", password="pass")
        group = Group.objects.create(name="HR")
        user.groups.add(group)
        self.assertTrue(EmployeePermission.can_manage_employee(user))
        self.assertTrue(EmployeePermission.can_edit_employee(user))
        self.assertTrue(EmployeePermission.can_delete_employee(user))

    def test_regular_employee_cannot_manage_employees(self):
        user = User.objects.create_user(username="employee", password="pass")
        group = Group.objects.create(name="EMPLOYEE")
        user.groups.add(group)
        self.assertFalse(EmployeePermission.can_manage_employee(user))
        self.assertFalse(EmployeePermission.can_edit_employee(user))
        self.assertFalse(EmployeePermission.can_delete_employee(user))


class EmployeeAPITests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="apiuser", password="pass")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_employee_list_requires_authentication(self):
        client = APIClient()
        response = client.get("/api/employees/")
        self.assertIn(response.status_code, [401, 403])

    def test_authenticated_user_can_list_employees(self):
        Employee.objects.create(name="John", email="john@example.com")
        response = self.client.get("/api/employees/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_create_employee_creates_account(self):
        payload = {
            "name": "Alice Smith",
            "email": "alice@example.com",
            "department": "IT",
            "designation": "Software Engineer",
            "joining_date": date.today().isoformat(),
        }
        response = self.client.post("/api/employees/create/", payload, format="json")

        self.assertEqual(response.status_code, 201)
        employee = Employee.objects.get(email="alice@example.com")
        self.assertIsNotNone(employee.user)
        self.assertTrue(employee.user.groups.filter(name="EMPLOYEE").exists())
