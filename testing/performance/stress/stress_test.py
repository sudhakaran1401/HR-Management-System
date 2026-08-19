from locust import HttpUser, LoadTestShape, between, task


class HRMSStressUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def open_home_page(self):
        self.client.get("/", name="GET /")


class HRMSStressShape(LoadTestShape):
    stages = [
        {"duration": 60, "users": 10, "spawn_rate": 2},
        {"duration": 120, "users": 50, "spawn_rate": 5},
        {"duration": 180, "users": 100, "spawn_rate": 10},
        {"duration": 240, "users": 250, "spawn_rate": 25},
        {"duration": 300, "users": 500, "spawn_rate": 50},
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                return stage["users"], stage["spawn_rate"]

        return None