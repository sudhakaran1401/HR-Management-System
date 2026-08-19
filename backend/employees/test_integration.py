from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from employees.models import Employee


class EmployeeAPIIntegrationTests(TestCase):
    """Integration tests for employee API -> serializer -> database -> account creation."""

    def setUp(self):
        self.user = User.objects.create_user(username="hr_api", password="pass")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_employee_then_retrieve_it_from_list(self):
        payload = {
            "name": "Integration Employee",
            "email": "integration.employee@example.com",
            "department": "IT",
            "designation": "Software Engineer",
            "joining_date": date(2026, 8, 11).isoformat(),
        }

        create_response = self.client.post(
            "/api/employees/create/", payload, format="json"
        )

        self.assertEqual(create_response.status_code, 201)
        employee_id = create_response.data["id"]
        employee = Employee.objects.get(pk=employee_id)
        self.assertIsNotNone(employee.user)

        list_response = self.client.get("/api/employees/")
        self.assertEqual(list_response.status_code, 200)
        self.assertTrue(any(item["id"] == employee_id for item in list_response.data))

    def test_employee_update_then_detail_returns_updated_data(self):
        employee = Employee.objects.create(
            name="Before Update",
            email="before@example.com",
            department="IT",
            designation="Software Engineer",
        )

        update_response = self.client.patch(
            f"/api/employees/{employee.id}/update/",
            {"name": "After Update"},
            format="json",
        )
        self.assertEqual(update_response.status_code, 200)

        detail_response = self.client.get(f"/api/employees/{employee.id}/")
        self.assertEqual(detail_response.status_code, 200)
        self.assertEqual(detail_response.data["name"], "After Update")
