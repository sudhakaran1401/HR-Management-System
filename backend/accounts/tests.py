from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from accounts.services.auth_service import AuthService
from employees.models import Employee, EmployeeProfile


class AuthenticationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="hruser", email="hr@example.com", password="StrongPass123!"
        )
        self.hr_group = Group.objects.create(name="HR")
        self.user.groups.add(self.hr_group)

    def test_auth_service_authenticates_valid_credentials(self):
        user = AuthService.authenticate_user(
            None, "hruser", "StrongPass123!"
        )
        self.assertEqual(user, self.user)

    def test_auth_service_rejects_invalid_credentials(self):
        user = AuthService.authenticate_user(
            None, "hruser", "wrong-password"
        )
        self.assertIsNone(user)

    def test_login_redirects_hr_user_to_hr_dashboard(self):
        response = self.client.post(
            reverse("login"),
            {"username": "hruser", "password": "StrongPass123!"},
        )
        self.assertRedirects(response, reverse("hr_dashboard"))

    def test_login_rejects_invalid_credentials(self):
        response = self.client.post(
            reverse("login"),
            {"username": "hruser", "password": "wrong-password"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,"Invalid Credentials")

    def test_logout_redirects_to_login(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("logout"))
        self.assertRedirects(response, reverse("login"))

    def test_current_user_api_requires_authentication(self):
        response = self.client.get("/api/me/")
        self.assertIn(response.status_code, [401, 403])

    def test_current_user_api_returns_user_and_hr_flag(self):
        employee = Employee.objects.create(
            name="HR User",
            email="hr@example.com",
            department="HR",
            designation="HR Manager",
        )
        EmployeeProfile.objects.create(user=self.user, employee=employee)

        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.get("/api/me/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], "hruser")
        self.assertTrue(response.data["is_hr"])
