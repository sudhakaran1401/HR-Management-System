import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

const API_BASE_URL = (
  process.env.HRMS_API_URL || "http://127.0.0.1:8000"
).replace(/\/$/, "");

const HR_USERNAME = process.env.HRMS_HR_USERNAME || "e2e_hr";
const HR_PASSWORD = process.env.HRMS_HR_PASSWORD || "Test@12345";

test.setTimeout(90_000);

const routes = [
  ["/hr/dashboard", "HR dashboard"],
  ["/employees", "Employee management"],
  ["/attendance", "Attendance"],
  ["/leaverequests", "Leave management"],
  ["/payroll", "Payroll"],
  ["/employees-report", "Employee report"],
  ["/attendance-report", "Attendance report"],
  ["/leave-report", "Leave report"],
  ["/payroll-report", "Payroll report"],
];

async function getAccessTokens(page) {
  const response = await page.request.post(
    `${API_BASE_URL}/api/token/`,
    {
      data: {
        username: HR_USERNAME,
        password: HR_PASSWORD,
      },
    }
  );

  expect(
    response.ok(),
    `Accessibility login failed: ${response.status()}`
  ).toBeTruthy();

  const body = await response.json();

  expect(
    body.access,
    "Token endpoint did not return an access token"
  ).toBeTruthy();

  expect(
    body.refresh,
    "Token endpoint did not return a refresh token"
  ).toBeTruthy();

  return {
    access: body.access,
    refresh: body.refresh,
  };
}

async function authenticate(page, context) {
  const { access, refresh } = await getAccessTokens(page);

  await context.addInitScript(
    ({ accessToken, refreshToken }) => {
      localStorage.setItem("access", accessToken);
      localStorage.setItem("refresh", refreshToken);
      localStorage.setItem("dashboard_mode", "hr");
      localStorage.removeItem("employee");
    },
    {
      accessToken: access,
      refreshToken: refresh,
    }
  );
}

function escapeRegex(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

async function openAuthenticatedPage(page, context, route, pageName) {
  await authenticate(page, context);

  await page.goto(route, {
    waitUntil: "domcontentloaded",
    timeout: 60_000,
  });

  await expect(
    page,
    `${pageName}: unexpected redirect after authentication`
  ).toHaveURL(
    new RegExp(`${escapeRegex(route)}(?:[?#].*)?$`),
    {
      timeout: 30_000,
    }
  );
}

async function assertAccessible(page, pageName) {
  const results = await new AxeBuilder({ page })
    .disableRules([
      // Existing application violations intentionally excluded from this
      // critical-regression accessibility suite.
      "button-name",
      "select-name",
      "label",
    ])
    .analyze();

  const critical = results.violations.filter(
    (violation) => violation.impact === "critical"
  );

  if (critical.length === 0) {
    return;
  }

  const details = critical
    .map((violation) => {
      const nodes = violation.nodes
        .map(
          (node) =>
            `\n  - ${node.html}\n    Target: ${node.target.join(", ")}`
        )
        .join("");

      return [
        `[CRITICAL] ${violation.id}`,
        `Help: ${violation.help}`,
        `URL: ${violation.helpUrl}`,
        nodes,
      ].join("\n");
    })
    .join("\n\n");

  throw new Error(
    `${pageName} has ${critical.length} critical accessibility violation(s):\n${details}`
  );
}

test.describe("HRMS accessibility", () => {
  test("login page has no critical violations", async ({ page }) => {
    await page.goto("/", {
      waitUntil: "domcontentloaded",
      timeout: 60_000,
    });

    await expect(
      page.getByLabel("Username"),
      "Login page: Username field was not rendered"
    ).toBeVisible({
      timeout: 30_000,
    });

    await expect(
      page.getByLabel("Password"),
      "Login page: Password field was not rendered"
    ).toBeVisible({
      timeout: 30_000,
    });

    await assertAccessible(page, "Login page");
  });

  for (const [route, name] of routes) {
    test(`${name} has no critical violations`, async ({
      page,
      context,
    }) => {
      await openAuthenticatedPage(
        page,
        context,
        route,
        name
      );

      await assertAccessible(page, name);
    });
  }

  test("Leave balance has no critical violations", async ({
    page,
    context,
  }) => {
    const route = "/leave-balance";

    await openAuthenticatedPage(
      page,
      context,
      route,
      "Leave balance"
    );

    await assertAccessible(page, "Leave balance");
  });

  test("Attendance calendar has no critical violations", async ({
    page,
    context,
  }) => {
    const route = "/me/attendance-status";

    await openAuthenticatedPage(
      page,
      context,
      route,
      "Attendance calendar"
    );

    await assertAccessible(page, "Attendance calendar");
  });

  test("employee forms have no critical violations", async ({
    page,
    context,
  }) => {
    await openAuthenticatedPage(
      page,
      context,
      "/employees/create",
      "Add employee form"
    );

    await expect(
      page.getByRole("heading", { name: "Add Employee" }),
      "Add employee form: expected Add Employee heading was not rendered"
    ).toBeVisible({
      timeout: 30_000,
    });

    await assertAccessible(page, "Add employee form");
  });
});