from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from employees.models import Employee, EmployeeProfile


class AuthenticationAPIIntegrationTests(TestCase):
    """Integration tests for JWT authentication -> authenticated API access."""

    def setUp(self):
        self.password = "StrongPass123!"
        self.user = User.objects.create_user(
            username="integration_user",
            email="integration@example.com",
            password=self.password,
        )
        self.employee = Employee.objects.create(
            name="Integration User",
            email="integration@example.com",
            department="IT",
            designation="Software Engineer",
        )
        EmployeeProfile.objects.create(user=self.user, employee=self.employee)
        self.client = APIClient()

    def test_login_token_can_authenticate_current_user_request(self):
        token_response = self.client.post(
            "/api/token/",
            {"username": self.user.username, "password": self.password},
            format="json",
        )

        self.assertEqual(token_response.status_code, 200)
        self.assertIn("access", token_response.data)
        self.assertIn("refresh", token_response.data)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token_response.data['access']}"
        )
        me_response = self.client.get("/api/me/")

        self.assertEqual(me_response.status_code, 200)
        self.assertEqual(me_response.data["username"], self.user.username)
        self.assertFalse(me_response.data["is_hr"])

    def test_invalid_credentials_do_not_issue_token(self):
        response = self.client.post(
            "/api/token/",
            {"username": self.user.username, "password": "wrong-password"},
            format="json",
        )

        self.assertEqual(response.status_code, 401)
        self.assertNotIn("access", response.data)
