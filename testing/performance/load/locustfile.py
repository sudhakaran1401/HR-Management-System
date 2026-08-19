import os

from locust import HttpUser, task, between
from locust.exception import StopUser


class HRMSLoadUser(HttpUser):
    """
    HRMS performance/load test user.

    The test authenticates using the seeded E2E HR account and then
    repeatedly exercises read-heavy HRMS API operations.
    """

    wait_time = between(1, 3)

    username = os.getenv("HRMS_LOAD_USERNAME", "e2e_hr")
    password = os.getenv("HRMS_LOAD_PASSWORD", "Test@12345")

    def on_start(self):
        """Authenticate once when a simulated user starts."""

        response = self.client.post(
            "/api/token/",
            json={
                "username": self.username,
                "password": self.password,
            },
            name="POST /api/token/",
        )

        if response.status_code != 200:
            response.failure(
                f"Login failed: HTTP {response.status_code}"
            )
            raise StopUser()

        try:
            tokens = response.json()
            access_token = tokens["access"]
        except (ValueError, KeyError):
            response.failure("Login response did not contain an access token.")
            raise StopUser()

        self.client.headers.update(
            {
                "Authorization": f"Bearer {access_token}",
            }
        )

    @task(5)
    def employee_list(self):
        """Load employee listing."""
        self.client.get(
            "/api/employees/",
            name="GET /api/employees/",
        )

    @task(5)
    def attendance_list(self):
        """Load attendance records."""
        self.client.get(
            "/api/attendance/",
            name="GET /api/attendance/",
        )

    @task(5)
    def leave_list(self):
        """Load leave requests."""
        self.client.get(
            "/api/leave/",
            name="GET /api/leave/",
        )

    @task(4)
    def payroll_list(self):
        """Load payroll history."""
        self.client.get(
            "/api/payroll/",
            name="GET /api/payroll/",
        )

    @task(4)
    def hr_dashboard(self):
        """Load HR dashboard data."""
        self.client.get(
            "/api/dashboard/hr/",
            name="GET /api/dashboard/hr/",
        )

    @task(3)
    def current_user(self):
        """Load authenticated user information."""
        self.client.get(
            "/api/me/",
            name="GET /api/me/",
        )

    @task(3)
    def employee_profile(self):
        """Load the logged-in employee profile."""
        self.client.get(
            "/api/employees/me/",
            name="GET /api/employees/me/",
        )

    @task(3)
    def leave_balance(self):
        """Load leave balance."""
        self.client.get(
            "/api/leave/balance/",
            name="GET /api/leave/balance/",
        )

    @task(2)
    def employee_report(self):
        """Load employee report."""
        self.client.get(
            "/api/employees/download/csv",
            name="GET /api/employees/download/csv",
        )

    @task(2)
    def attendance_report(self):
        """Load attendance report."""
        self.client.get(
            "/api/attendance/report/",
            name="GET /api/attendance/report/",
        )

    @task(2)
    def leave_report(self):
        """Load leave report."""
        self.client.get(
            "/api/leave/report/",
            name="GET /api/leave/report/",
        )

    @task(2)
    def payroll_report(self):
        """Load payroll PDF report."""
        self.client.get(
            "/api/payroll/download/pdf/",
            name="GET /api/payroll/download/pdf/",
        )