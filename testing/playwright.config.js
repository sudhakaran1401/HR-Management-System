import { defineConfig, devices } from "@playwright/test";

const frontendUrl =
  process.env.HRMS_BASE_URL || "http://127.0.0.1:5173";

const apiUrl =
  process.env.HRMS_API_URL || "http://127.0.0.1:8000";

export default defineConfig({
  testDir: "./e2e",

  timeout: 45_000,

  expect: {
    timeout: 10_000,
  },

  fullyParallel: true,

  forbidOnly: !!process.env.CI,

  retries: process.env.CI ? 2 : 0,

  reporter: process.env.CI ? "line" : "html",

  use: {
    baseURL: frontendUrl,
    trace: "retain-on-failure",
    screenshot: "only-on-failure",
    video: "retain-on-failure",
  },

  webServer: [
    {
      command: "npm run dev -- --host 127.0.0.1",
      cwd: "../frontend",
      url: frontendUrl,
      reuseExistingServer: true,
      timeout: 120_000,
    },

    {
      command: "python manage.py runserver 127.0.0.1:8000",
      cwd: "../backend",
      url: `${apiUrl}/`,
      reuseExistingServer: true,
      timeout: 120_000,
    },
  ],

  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },

    {
      name: "firefox",
      use: { ...devices["Desktop Firefox"] },
    },

    {
      name: "webkit",
      use: { ...devices["Desktop Safari"] },
    },
  ],
});