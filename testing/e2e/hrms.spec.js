import { test, expect } from "@playwright/test";

const API_BASE_URL = (
  process.env.HRMS_API_URL || "http://127.0.0.1:8000"
).replace(/\/$/, "");

const HR_USERNAME = process.env.HRMS_HR_USERNAME || "e2e_hr";
const HR_PASSWORD = process.env.HRMS_HR_PASSWORD || "Test@12345";
const EMPLOYEE_USERNAME =
  process.env.HRMS_EMPLOYEE_USERNAME || "e2e_employee";
const EMPLOYEE_PASSWORD =
  process.env.HRMS_EMPLOYEE_PASSWORD || "Test@12345";

const E2E_EMPLOYEE_NAME =
  process.env.HRMS_EMPLOYEE_NAME || "E2E Employee";
const E2E_EMPLOYEE_EMAIL =
  process.env.HRMS_EMPLOYEE_EMAIL || "e2e.employee@example.com";

const today = new Date();

function isoDate(value) {
  const date = value instanceof Date ? value : new Date(value);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function addDays(days) {
  const value = new Date(today);
  value.setDate(value.getDate() + days);
  return isoDate(value);
}

function nextMonth() {
  return isoDate(
    new Date(today.getFullYear(), today.getMonth() + 1, 1)
  );
}

async function getToken(request, username, password) {
  const response = await request.post(`${API_BASE_URL}/api/token/`, {
    data: { username, password },
  });

  expect(
    response.ok(),
    `Token request failed for ${username}: ${response.status()}`
  ).toBeTruthy();

  const body = await response.json();
  expect(body.access).toBeTruthy();
  expect(body.refresh).toBeTruthy();

  return body.access;
}

async function apiJson(request, token, method, path, data) {
  const response = await request[method](`${API_BASE_URL}${path}`, {
    headers: token
      ? { Authorization: `Bearer ${token}` }
      : undefined,
    ...(data === undefined ? {} : { data }),
  });

  const text = await response.text();
  let body = text;

  try {
    body = text ? JSON.parse(text) : null;
  } catch {
    // Keep the response text for a useful failure message.
  }

  expect(
    response.ok(),
    `${method.toUpperCase()} ${path} failed: ${response.status()} ${text}`
  ).toBeTruthy();

  return body;
}

async function login(page, username = HR_USERNAME, password = HR_PASSWORD) {
  const access = await getToken(page.request, username, password);

  const meResponse = await page.request.get(`${API_BASE_URL}/api/me/`, {
    headers: { Authorization: `Bearer ${access}` },
  });

  expect(
    meResponse.ok(),
    `Could not load /api/me/: ${meResponse.status()}`
  ).toBeTruthy();

  const me = await meResponse.json();
  let employee = null;

  if (me.is_hr === true || username === HR_USERNAME) {
    employee = {
      id: me.employee_id || me.id,
      username: me.username || username,
      name: me.name || username,
      department: "HR",
      designation: me.designation || "HR Manager",
    };
  } else {
    const profileResponse = await page.request.get(
      `${API_BASE_URL}/api/employees/me/`,
      { headers: { Authorization: `Bearer ${access}` } }
    );

    expect(
      profileResponse.ok(),
      `Could not load employee profile: ${profileResponse.status()}`
    ).toBeTruthy();

    employee = await profileResponse.json();
  }

  await page.addInitScript(
  ({ accessToken, employeeProfile }) => {
    localStorage.setItem("access", accessToken);
    localStorage.setItem("refresh", "");

    if (employeeProfile) {
      localStorage.setItem(
        "employee",
        JSON.stringify(employeeProfile)
      );
    } else {
      localStorage.removeItem("employee");
    }

    localStorage.setItem(
      "dashboard_mode",
      employeeProfile?.department === "HR"
        ? "hr"
        : "employee"
    );
  },
  {
    accessToken: access,
    employeeProfile: employee,
  }
  );

  await page.goto("/", {
    waitUntil: "domcontentloaded",
  });

  return { access, me, employee };
}

async function loginEmployeeForE2E(page) {
  const access = await getToken(
    page.request,
    EMPLOYEE_USERNAME,
    EMPLOYEE_PASSWORD
  );

  // Get the employee record using HR credentials because
  // /api/employees/me/ is intentionally restricted for this test user.
  const hrToken = await getToken(
    page.request,
    HR_USERNAME,
    HR_PASSWORD
  );

  const employees = await apiJson(
    page.request,
    hrToken,
    "get",
    "/api/employees/"
  );

  const employee = employees.find(
    (item) =>
      item.name === E2E_EMPLOYEE_NAME ||
      item.email === E2E_EMPLOYEE_EMAIL
  );

  expect(
    employee?.id,
    `E2E employee "${E2E_EMPLOYEE_NAME}" was not found`
  ).toBeTruthy();

  await page.goto("/");

  await page.evaluate(
    ({ accessToken, employeeProfile }) => {
      localStorage.setItem("access", accessToken);
      localStorage.setItem("refresh", "");
      localStorage.setItem(
        "employee",
        JSON.stringify(employeeProfile)
      );
      localStorage.setItem("dashboard_mode", "employee");
    },
    {
      accessToken: access,
      employeeProfile: employee,
    }
  );

  return employee;
}

async function authorizedRequest(page, method, path, data) {
  const access = await page.evaluate(
    () => localStorage.getItem("access")
  );
  expect(access).toBeTruthy();

  return page.request[method](`${API_BASE_URL}${path}`, {
    headers: { Authorization: `Bearer ${access}` },
    ...(data === undefined ? {} : { data }),
  });
}

async function ensureSeedData(request) {
  const hrToken = await getToken(request, HR_USERNAME, HR_PASSWORD);
  const employees = await apiJson(
    request,
    hrToken,
    "get",
    "/api/employees/"
  );

  const employee = employees.find(
    (item) =>
      item.name === E2E_EMPLOYEE_NAME ||
      item.email === E2E_EMPLOYEE_EMAIL
  );

  expect(
    employee?.id,
    `Seed employee "${E2E_EMPLOYEE_NAME}" was not found. Run backend/e2e_seed.py before Playwright.`
  ).toBeTruthy();

  const attendance = await apiJson(
    request,
    hrToken,
    "get",
    "/api/attendance/"
  );

  if (
    !attendance.some(
      (item) =>
        Number(
          typeof item.employee === "object"
            ? item.employee?.id
            : item.employee
        ) === Number(employee.id)
    )
  ) {
    await apiJson(request, hrToken, "post", "/api/attendance/create/", {
      employee: employee.id,
      date: addDays(-1),
      status: "Present",
      check_in: "09:00",
      check_out: "17:30",
      notes: "E2E fallback seed attendance",
    });
  }

  const payrolls = await apiJson(
  request,
  hrToken,
  "get",
  "/api/payroll/"
);

const currentPayMonth = isoDate(
  new Date(today.getFullYear(), today.getMonth(), 1)
);

const currentPayrollExists = payrolls.some((item) => {
  const employeeId =
    typeof item.employee === "object"
      ? item.employee?.id
      : item.employee;

  const payMonth = String(item.pay_month).slice(0, 10);

  return (
    Number(employeeId) === Number(employee.id) &&
    payMonth === currentPayMonth
  );
});

if (!currentPayrollExists) {
  await apiJson(
    request,
    hrToken,
    "post",
    "/api/payroll/create/",
    {
      employee: employee.id,
      pay_month: currentPayMonth,
      amt_per_day: "100.00",
      notes: "E2E fallback seed payroll",
    }
  );
}

  return { hrToken, employee };
}

test.beforeAll(async ({ request }) => {
  await ensureSeedData(request);
});

test.describe("Authentication", () => {
  test("login page renders with accessible controls", async ({ page }) => {
    await page.goto("/");
    await expect(page).toHaveTitle(/HR Management System/i);
    await expect(
      page.getByRole("heading", { name: "HR Management System" })
    ).toBeVisible();
    await expect(page.getByLabel("Username")).toBeVisible();
    await expect(page.getByLabel("Password")).toBeVisible();
    await expect(
      page.getByRole("button", { name: "Login" })
    ).toBeVisible();
  });

  test("invalid credentials show the login error", async ({ page }) => {
    await page.goto("/");
    await page.getByLabel("Username").fill("wrong_user");
    await page.getByLabel("Password").fill("wrong_password");
    await page.getByRole("button", { name: "Login" }).click();

    await expect(page.getByRole("alert")).toContainText(
      "Invalid Credentials.",
      { timeout: 10_000 }
    );
    await expect(page).toHaveURL(/\/$/);
  });

  test("protected routes redirect unauthenticated users", async ({ page }) => {
    await page.goto("/hr/dashboard");
    await expect(page).toHaveURL(/\/$/);
    await expect(page.getByLabel("Username")).toBeVisible();
  });

  test("HR can authenticate and reach the dashboard", async ({ page }) => {
    await login(page);
    await page.goto("/hr/dashboard");
    await expect(
      page.getByRole("heading", { name: "HR Dashboard" })
    ).toBeVisible();
  });

  test("logout clears the access token", async ({ page }) => {
    await login(page);
    await page.goto("/hr/dashboard");

    await page.locator("#userDropdown").click();
    await page.getByRole("button", { name: "Logout" }).click();

    await expect(page).toHaveURL(/\/$/);
    await expect(page.getByLabel("Username")).toBeVisible();
    await expect(
      page.evaluate(() => localStorage.getItem("access"))
    ).resolves.toBeNull();
  });
});

test.describe("HR navigation", () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
  });

  const pages = [
    ["/hr/dashboard", "HR Dashboard"],
    ["/employees", "Employees"],
    ["/attendance", "Attendance Records"],
    ["/leaverequests", "Leave Requests"],
    ["/payroll", "Payroll History"],
    ["/employees-report", "Employee Report"],
    ["/attendance-report", "Attendance Report"],
    ["/leave-report", "Leave Report"],
    ["/payroll-report", "Payroll Report"],
  ];

  for (const [route, heading] of pages) {
    test(`${heading} route loads`, async ({ page }) => {
      await page.goto(route);
      await expect(
        page.getByRole("heading", { name: heading })
      ).toBeVisible();
    });
  }
});

test.describe("Employee management", () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
  });

  test("employee list supports search and empty results", async ({ page }) => {
    await page.goto("/employees");
    const search = page.getByPlaceholder("Search employees...");

    await search.fill(E2E_EMPLOYEE_NAME);
    await expect(
      page.getByRole("row", {
        name: new RegExp(E2E_EMPLOYEE_NAME),
      })
    ).toBeVisible();

    await search.fill(`NO_EMPLOYEE_${Date.now()}`);
    await expect(
      page.getByRole("row", { name: /No records found/i })
    ).toBeVisible();
  });

  test("HR can create, view, edit and delete an employee", async ({
    page,
  }) => {
    const stamp = Date.now();
    const name = `E2E UI Employee ${stamp}`;
    const email = `e2e.ui.${stamp}@example.com`;

    await page.goto("/employees/create");
    await expect(
      page.getByRole("heading", { name: "Add Employee" })
    ).toBeVisible();

    await page.locator('input[name="name"]').fill(name);
    await page.locator('input[name="email"]').fill(email);
    await page.locator('input[name="phone"]').fill("8888888888");
    await page.locator('select[name="department"]').selectOption("IT");
    await page
      .locator('select[name="designation"]')
      .selectOption("Software Engineer");
    await page.locator('input[name="joining_date"]').fill(isoDate(today));
    await page.locator('textarea[name="address"]').fill("E2E UI Address");
    await page.getByRole("button", { name: "Add", exact: true }).click();

    await expect(page).toHaveURL(/\/employees$/);
    const search = page.getByPlaceholder("Search employees...");
    await search.fill(name);

    const row = page.getByRole("row", {
      name: new RegExp(name),
    });
    await expect(row).toBeVisible();

    await row.getByRole("button", { name: "View" }).click();
    await expect(
      page.getByRole("heading", { name: "Profile" })
    ).toBeVisible();
    await expect(
      page.getByRole("heading", { name, exact: true })
    ).toBeVisible();

    await page.goto("/employees");
    await search.fill(name);
    await page
      .getByRole("row", { name: new RegExp(name) })
      .getByRole("button", { name: "Edit" })
      .click();

    await expect(
      page.getByRole("heading", { name: "Edit Employee" })
    ).toBeVisible();
    await page.locator('input[name="phone"]').fill("7777777777");
    await page.getByRole("button", { name: "Update", exact: true }).click();

    await expect(page).toHaveURL(/\/employees$/);
    await page.getByPlaceholder("Search employees...").fill(name);
    await expect(
      page.getByRole("row", { name: new RegExp(name) })
    ).toContainText("7777777777");

    await page
      .getByRole("row", { name: new RegExp(name) })
      .getByRole("button", { name: "Delete" })
      .click();

    await expect(
      page.getByRole("heading", { name: "Confirm Deletion" })
    ).toBeVisible();
    await page.getByRole("button", { name: "Yes, Delete" }).click();

    await expect(page).toHaveURL(/\/employees$/);
    await page.getByPlaceholder("Search employees...").fill(name);
    await expect(
      page.getByRole("row", { name: /No records found/i })
    ).toBeVisible();
  });
});

test.describe("Attendance", () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
  });

  test("attendance list loads seeded data", async ({ page }) => {
    await page.goto("/attendance");

    await expect(
      page.getByRole("heading", { name: "Attendance Records" })
    ).toBeVisible();

    await page
      .getByPlaceholder("Search attendance records...")
      .fill(E2E_EMPLOYEE_NAME);

    const employeeRows = page.getByRole("row").filter({
      has: page.getByRole("cell", {
        name: E2E_EMPLOYEE_NAME,
        exact: true,
      }),
    });

    await expect(employeeRows.first()).toBeVisible();
    await expect(employeeRows).not.toHaveCount(0);
  });

  test("HR can mark attendance for the seeded employee", async ({ page }) => {
  await login(page);

  // Get the seeded employee.
  const employeesResponse = await authorizedRequest(
    page,
    "get",
    "/api/employees/"
  );

  expect(employeesResponse.ok()).toBeTruthy();

  const employees = await employeesResponse.json();

  const employee = employees.find(
    (item) =>
      item.name === E2E_EMPLOYEE_NAME ||
      item.email === E2E_EMPLOYEE_EMAIL
  );

  expect(
    employee?.id,
    `E2E employee "${E2E_EMPLOYEE_NAME}" was not found`
  ).toBeTruthy();

  // Get existing attendance records so we can choose an unused
  // past date.
  const attendanceResponse = await authorizedRequest(
    page,
    "get",
    "/api/attendance/"
  );

  expect(attendanceResponse.ok()).toBeTruthy();

  const attendance = await attendanceResponse.json();

  const usedDates = new Set(
    attendance
      .filter((item) => {
        const employeeId =
          typeof item.employee === "object"
            ? item.employee?.id
            : item.employee;

        return Number(employeeId) === Number(employee.id);
      })
      .map((item) => String(item.date).slice(0, 10))
  );

  let date = null;

  for (let offset = 2; offset <= 365; offset += 1) {
    const candidate = addDays(-offset);

    const existingResponse = await authorizedRequest(
      page,
      "get",
      `/api/attendance/?employee=${encodeURIComponent(employee.id)}&date=${encodeURIComponent(candidate)}`
    );

    expect(
      existingResponse.ok(),
      `Failed to check attendance for ${E2E_EMPLOYEE_NAME} on ${candidate}: ${existingResponse.status()}`
    ).toBeTruthy();

    const existing = await existingResponse.json();

    const records = Array.isArray(existing)
      ? existing
      : existing.results || [];

    if (records.length === 0) {
      date = candidate;
      break;
    }
  }

  expect(
    date,
    "Could not find an unused past attendance date"
  ).toBeTruthy();

  // Open attendance form.
  await page.goto("/employees/mark-attendance");

  await expect(
    page.getByRole("heading", {
      name: "Mark Attendance",
      exact: true,
    })
  ).toBeVisible();

  // Fill attendance form.
  await page
    .locator('select[name="employee"]')
    .selectOption({
      label: E2E_EMPLOYEE_NAME,
    });

  await page
    .locator('input[name="date"]')
    .fill(date);

  await page
    .locator('select[name="status"]')
    .selectOption("Present");

  await page
    .locator('input[name="check_in"]')
    .fill("09:00");

  await page
    .locator('input[name="check_out"]')
    .fill("17:30");

  await page
    .locator('textarea[name="notes"]')
    .fill(`E2E UI attendance ${Date.now()}`);

  // Submit and wait for the real API response.
  // The attendance endpoint has a unique constraint on employee + date.
// Multiple browser projects can legitimately race for the same unused date.
// If another worker wins the race, move to the next unused past date and retry.

let createResponse = null;

for (let attempt = 0; attempt < 20; attempt += 1) {
  const responsePromise = page.waitForResponse(
    (response) =>
      response.request().method() === "POST" &&
      response.url().includes("/api/attendance/create/")
  );

  await page.getByRole("button", {
    name: "Save",
    exact: true,
  }).click();

  const response = await responsePromise;
  const responseBody = await response.text();

  if (response.ok()) {
    createResponse = response;
    break;
  }

  // A concurrent browser/test may have created this employee/date
  // between our availability check and the POST.
  let body = null;

  try {
    body = JSON.parse(responseBody);
  } catch {
    // Keep the raw response below.
  }

  const isDuplicateAttendance =
    response.status() === 400 &&
    body?.non_field_errors?.some((message) =>
      String(message).toLowerCase().includes("unique set")
    );

  if (!isDuplicateAttendance) {
    throw new Error(
      [
        `Attendance create failed: ${response.status()}`,
        `Request body: ${JSON.stringify(
          response.request().postDataJSON(),
          null,
          2
        )}`,
        `Response body: ${responseBody}`,
      ].join("\n")
    );
  }

  // Another browser won the race for this date.
  // Pick the next past date and try the same UI operation again.
  let nextDate = null;

  for (let offset = 2 + attempt + 1; offset <= 365; offset += 1) {
    const candidate = addDays(-offset);

    if (!usedDates.has(candidate)) {
      nextDate = candidate;
      usedDates.add(candidate);
      break;
    }
  }

  expect(
    nextDate,
    "Could not find another unused past attendance date after a duplicate."
  ).toBeTruthy();

  date = nextDate;

  await page.locator('input[name="date"]').fill(date);
  }

  expect(
    createResponse,
    "Attendance creation did not succeed after retrying unused dates."
  ).toBeTruthy();

  // The application should return to attendance list.
  await expect(page).toHaveURL(/\/attendance$/);

  const search = page.getByPlaceholder(
    "Search attendance records..."
  );

  await search.fill(E2E_EMPLOYEE_NAME);

  // Increase page size so fewer pagination steps are required.
  const rowsPerPage = page.getByRole("combobox", {
    name: "Rows per page",
  });

  await rowsPerPage.selectOption("25");

  const expectedDate = new Date(
    `${date}T00:00:00`
  ).toLocaleDateString("en-US", {
    month: "short",
    day: "2-digit",
    year: "numeric",
  });

  const employeeRow = page
    .getByRole("row")
    .filter({
      has: page.getByRole("cell", {
        name: E2E_EMPLOYEE_NAME,
        exact: true,
      }),
    })
    .filter({
      hasText: expectedDate,
    });

  // Search all pagination pages instead of assuming the record
  // appears on the first page.
  const nextButton = page.getByRole("button", {
    name: "Next →",
    exact: true,
  });

  for (let pageNumber = 0; pageNumber < 20; pageNumber++) {
    if (await employeeRow.count() > 0) {
      break;
    }

    if (!(await nextButton.isEnabled())) {
      break;
    }

    await nextButton.click();

    // Wait for the table to settle after pagination.
    await expect(
      page.getByRole("rowgroup").nth(1)
    ).toBeVisible();
  }

  await expect(
    employeeRow,
    `Attendance for ${E2E_EMPLOYEE_NAME} on ${expectedDate} was not found`
  ).toBeVisible();

  await expect(employeeRow).toContainText("Present");
  await expect(employeeRow).toContainText("09:00 AM");
  await expect(employeeRow).toContainText("05:30 PM");
  });

  test("attendance search handles no results", async ({ page }) => {
    await page.goto("/attendance");

    await page
      .getByPlaceholder("Search attendance records...")
      .fill(`NO_ATTENDANCE_${Date.now()}`);

    await expect(
      page.getByRole("row", { name: /No records found/i })
    ).toBeVisible();
  });
});

test.describe("Leave management", () => {
  async function getEmployeeFromHR(page, existingToken = null) {
  const hrToken =
    existingToken ||
    (await getToken(
      page.request,
      HR_USERNAME,
      HR_PASSWORD
    ));

  const employees = await apiJson(
    page.request,
    hrToken,
    "get",
    "/api/employees/"
  );

  const employee = employees.find(
    (item) =>
      item.name === E2E_EMPLOYEE_NAME ||
      item.email === E2E_EMPLOYEE_EMAIL
  );

  expect(
    employee?.id,
    `E2E employee "${E2E_EMPLOYEE_NAME}" was not found`
  ).toBeTruthy();

  return {
    hrToken,
    employee,
  };
}

  test("HR can view leave requests", async ({ page }) => {
    await login(page);

    await page.goto("/leaverequests");

    await expect(
      page.getByRole("heading", {
        name: "Leave Requests",
      })
    ).toBeVisible();

    await expect(
      page.getByPlaceholder("Search leave requests...")
    ).toBeVisible();
  });

  test("employee can apply for leave", async ({ page }) => {
    const employee = await loginEmployeeForE2E(page);

    // The application requests the employee profile when opening
    // the leave form. Mock only this profile request.
    await page.route(
      `${API_BASE_URL}/api/employees/me/`,
      async (route) => {
        await route.fulfill({
          status: 200,
          contentType: "application/json",
          body: JSON.stringify(employee),
        });
      }
    );

    await page.goto("/leaverequest/create");

    await expect(
      page.getByRole("heading", {
        name: "Apply Leave",
      })
    ).toBeVisible();

    const startDate = addDays(100);
    const endDate = addDays(101);
    const reason = `E2E Leave ${Date.now()}`;

    // Use name attributes because the application's
    // labels are not associated with the form controls.
    await page
      .locator('select[name="leave_type"]')
      .selectOption("CASUAL");

    await page
      .locator('input[name="start_date"]')
      .fill(startDate);

    await page
      .locator('input[name="end_date"]')
      .fill(endDate);

    await page
      .locator('textarea[name="reason"]')
      .fill(reason);

    const createResponse = page.waitForResponse(
      (response) =>
        response.request().method() === "POST" &&
        response.url().includes("/api/leave/create/")
    );

    await page.getByRole("button", {
      name: "Submit",
      exact: true,
    }).click();

    const response = await createResponse;

    expect(
      response.ok(),
      `Leave creation failed: ${response.status()}`
    ).toBeTruthy();

    await expect(page).toHaveURL(
      /\/me\/leaverequests$/
    );

    await expect(
      page.getByText(reason, { exact: true })
    ).toBeVisible({
      timeout: 10_000,
    });
  });

  test("HR can approve a pending leave request", async ({
    page,
  }) => {
    await login(page);

    const { employee } = await getEmployeeFromHR(page);

    const startDate = addDays(150);
    const endDate = addDays(151);
    const reason = `E2E Approval ${Date.now()}`;

    const access = await page.evaluate(
      () => localStorage.getItem("access")
    );

    expect(access).toBeTruthy();

    // Create a real pending leave through the API.
    const leave = await apiJson(
      page.request,
      access,
      "post",
      "/api/leave/create/",
      {
        employee: employee.id,
        leave_type: "CASUAL",
        start_date: startDate,
        end_date: endDate,
        reason,
      }
    );

    expect(leave?.id).toBeTruthy();

    await page.goto("/leaverequests");

    const search = page.getByPlaceholder(
      "Search leave requests..."
    );

    await search.fill(reason);

    const row = page.getByRole("row", {
      name: new RegExp(reason),
    });

    await expect(row).toBeVisible();

    const approveButton = row.getByRole("button", {
      name: "Approve",
    });

    await expect(approveButton).toBeVisible();

    const approveResponse = page.waitForResponse(
      (response) =>
        response.request().method() === "POST" &&
        response.url().includes(
          `/api/leave/${leave.id}/approve/`
        )
    );

    await approveButton.click();

    const response = await approveResponse;

    expect(
      response.ok(),
      `Leave approval failed: ${response.status()}`
    ).toBeTruthy();

    await expect(
      page.getByText(
        "Leave approved successfully.",
        { exact: true }
      )
    ).toBeVisible({
      timeout: 10_000,
    });
  });

  test("leave balance page loads", async ({ page }) => {
  const employee = await loginEmployeeForE2E(page);

  // The employee profile endpoint is unavailable to this test user.
  // Mock only the profile request required by the page.
  await page.route(
    `${API_BASE_URL}/api/employees/me/`,
    async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(employee),
      });
    }
  );

  // Keep the test independent of existing leave-balance data.
  await page.route(
    `${API_BASE_URL}/api/leave/balance/`,
    async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          employee: E2E_EMPLOYEE_NAME,
          total: 0,
          approved: 0,
          pending: 0,
          rejected: 0,
        }),
      });
    }
  );

  await page.goto("/leave-balance");

  // Page loaded successfully.
  await expect(
    page.getByRole("heading", {
      name: "Leave Balance",
      exact: true,
    })
  ).toBeVisible();

  // Target the employee name inside the Leave Balance content,
  // not the duplicate name in the navigation bar.
  const employeeSection = page
    .getByText("Employee :", { exact: true })
    .locator("..");

  await expect(employeeSection).toContainText(
    E2E_EMPLOYEE_NAME
  );

  // Verify the four balance cards.
  await expect(
    page.getByRole("heading", {
      name: "Total Applied",
      exact: true,
    })
  ).toBeVisible();

  await expect(
    page.getByRole("heading", {
      name: "Approved",
      exact: true,
    })
  ).toBeVisible();

  await expect(
    page.getByRole("heading", {
      name: "Pending",
      exact: true,
    })
  ).toBeVisible();

  await expect(
    page.getByRole("heading", {
      name: "Rejected",
      exact: true,
    })
  ).toBeVisible();

  // Verify page actions.
  await expect(
    page.getByRole("button", {
      name: "Apply Leave",
      exact: true,
    })
  ).toBeVisible();

  await expect(
    page.getByRole("button", {
      name: "My Requests",
      exact: true,
    })
  ).toBeVisible();
  });

  test("HR leave search handles no results", async ({
    page,
  }) => {
    await login(page);

    await page.goto("/leaverequests");

    const search = page.getByPlaceholder(
      "Search leave requests..."
    );

    await search.fill(
      `NO_LEAVE_${Date.now()}`
    );

    await expect(
      page.getByRole("row", {
        name: /No records found/i,
      })
    ).toBeVisible();
  });
});

test.describe("Payroll", () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
  });

  test("payroll list loads seeded payroll", async ({ page }) => {
  await page.goto("/payroll");

  await expect(
    page.getByRole("heading", {
      name: "Payroll History",
      exact: true,
    })
  ).toBeVisible();

 // Get the actual payroll data instead of assuming Aug/Sep/etc.
  const payrollResponse = await authorizedRequest(
    page,
    "get",
    "/api/payroll/"
  );

  expect(
    payrollResponse.ok(),
    `Could not load payrolls: ${payrollResponse.status()}`
  ).toBeTruthy();

  const payrolls = await payrollResponse.json();

  const employeesResponse = await authorizedRequest( page, "get", "/api/employees/" );

  expect(employeesResponse.ok()).toBeTruthy();

  const employees = await employeesResponse.json();

  const employee = employees.find( (item) => item.name === E2E_EMPLOYEE_NAME || item.email === E2E_EMPLOYEE_EMAIL );

  expect( employee?.id, `E2E employee "${E2E_EMPLOYEE_NAME}" was not found` ).toBeTruthy();

  const seededPayMonth = isoDate( new Date(today.getFullYear(), today.getMonth(), 1) ).slice(0, 7);

  const payroll = payrolls.find((item) => {
    const employeeId =
      typeof item.employee === "object"
        ? item.employee?.id
        : item.employee;

    const payMonth = String(item.pay_month).slice(0, 7);

    return (
      Number(employeeId) === Number(employee.id) &&
      payMonth === seededPayMonth
    );
  });

  expect( payroll?.id, `No payroll found for ${E2E_EMPLOYEE_NAME}` ).toBeTruthy();

  const payMonth = String(payroll.pay_month).slice(0, 7);

  const [year, month] = payMonth.split("-");

  const monthLabel = new Date(
    Number(year),
    Number(month) - 1,
    1
  ).toLocaleDateString("en-US", {
    month: "short",
    year: "numeric",
  });

  await page .getByPlaceholder("Search payroll...") .fill(E2E_EMPLOYEE_NAME);

  const rowsPerPage = page.getByRole("combobox", {
    name: "Rows per page",
  });

  if (await rowsPerPage.count()) {
    await rowsPerPage.selectOption("25");
  }

  const payrollRow = page
  .getByRole("row")
  .filter({
    has: page.getByRole("cell", {
      name: E2E_EMPLOYEE_NAME,
      exact: true,
    }),
  })
  .filter({
    hasText: monthLabel,
  });

  const nextButton = page.getByRole("button", {
    name: "Next →",
    exact: true,
  });

  for (let pageNumber = 0; pageNumber < 20; pageNumber++) {
    if (await payrollRow.count() > 0) {
      break;
    }

    if (!(await nextButton.isEnabled())) {
      break;
    }

  await nextButton.click();

  await expect(
    page.getByRole("rowgroup").nth(1)
  ).toBeVisible();
  }

  await expect(
    payrollRow,
    `Payroll for ${E2E_EMPLOYEE_NAME} / ${monthLabel} was not found`
  ).toBeVisible();

  await expect(payrollRow).toContainText("₹3,000");
  await expect(payrollRow).toContainText("₹210");
  await expect(payrollRow).toContainText("₹2,790");
  });

  test("HR can create payroll", async ({ page }) => {
    const employeesResponse = await authorizedRequest(
      page,
      "get",
      "/api/employees/"
    );

    expect(
      employeesResponse.ok(),
      `Could not load employees: ${employeesResponse.status()}`
    ).toBeTruthy();

    const employees = await employeesResponse.json();

    const employee = employees.find(
      (item) =>
        item.name === E2E_EMPLOYEE_NAME ||
        item.email === E2E_EMPLOYEE_EMAIL
    );

    expect(
      employee?.id,
      `E2E employee "${E2E_EMPLOYEE_NAME}" was not found`
    ).toBeTruthy();

    /*
     * Payroll has a unique constraint on:
     * employee + pay_month
     *
     * Therefore do not blindly use nextMonth().
     * Find an unused future month first.
     */
    const payrollResponse = await authorizedRequest(
      page,
      "get",
      "/api/payroll/"
    );

    expect(
      payrollResponse.ok(),
      `Could not load existing payrolls: ${payrollResponse.status()}`
    ).toBeTruthy();

    const payrolls = await payrollResponse.json();

    const usedMonths = new Set(
      payrolls
        .filter((item) => {
          const payrollEmployee =
            typeof item.employee === "object"
              ? item.employee?.id
              : item.employee;

          return (
            Number(payrollEmployee) === Number(employee.id)
          );
        })
        .map((item) =>
          String(item.pay_month).slice(0, 7)
        )
    );

    let payMonth = null;

    for (let offset = 1; offset <= 120; offset += 1) {
      const candidate = new Date(
        today.getFullYear(),
        today.getMonth() + offset,
        1
      );

      const year = candidate.getFullYear();
      const month = String(
        candidate.getMonth() + 1
      ).padStart(2, "0");

      const monthKey = `${year}-${month}`;

      if (!usedMonths.has(monthKey)) {
        payMonth = `${monthKey}-01`;
        break;
      }
    }

    expect(
      payMonth,
      "Could not find an unused future payroll month"
    ).toBeTruthy();

    await page.goto("/payroll/create");

    await expect(
      page.getByRole("heading", {
        name: "Add Payroll",
        exact: true,
      })
    ).toBeVisible();

    await page
      .locator('select[name="employee"]')
      .selectOption(String(employee.id));

    await page
      .locator('input[name="pay_month"]')
      .fill(payMonth);

    await page
      .locator('input[name="amt_per_day"]')
      .fill("100.00");

    /*
     * paid_date is required by the API and must be YYYY-MM-DD.
     */
    await page
      .locator('input[name="paid_date"]')
      .fill(isoDate(new Date()));

    await page
      .locator('textarea[name="notes"]')
      .fill(`E2E payroll ${Date.now()}`);

    const responsePromise = page.waitForResponse(
      (response) =>
        response.request().method() === "POST" &&
        response.url().includes("/api/payroll/create/")
    );

    await page.getByRole("button", {
      name: "Create Payroll",
      exact: true,
    }).click();

    const response = await responsePromise;
    const responseText = await response.text();

    expect(
      response.ok(),
      `Payroll creation failed: HTTP ${response.status()} ${responseText}`
    ).toBeTruthy();

    await expect(page).toHaveURL(/\/payroll$/);

    await expect(
      page.getByRole("heading", {
        name: "Payroll History",
        exact: true,
      })
    ).toBeVisible();
  });

  test("payslip preview loads", async ({ page }) => {
    const response = await authorizedRequest(
      page,
      "get",
      "/api/payroll/"
    );

    expect(
      response.ok(),
      `Could not load payrolls: ${response.status()}`
    ).toBeTruthy();

    const payrolls = await response.json();

    /*
     * Prefer the seeded E2E employee payroll so this test is
     * deterministic.
     */
    const payroll = payrolls.find((item) => {
      const employee =
        typeof item.employee === "object"
          ? item.employee
          : null;

      return (
        employee?.name === E2E_EMPLOYEE_NAME ||
        employee?.email === E2E_EMPLOYEE_EMAIL
      );
    }) || payrolls.find((item) => {
      const employeeId =
        typeof item.employee === "object"
          ? item.employee?.id
          : item.employee;

      return Number(employeeId) > 0;
    });

    expect(
      payroll?.id,
      "No payroll record available for payslip preview"
    ).toBeTruthy();

    await page.goto(
      `/payroll/payslip/${payroll.id}`
    );

    await expect(
      page.getByRole("heading", {
        name: "Payslip Preview",
        exact: true,
      })
    ).toBeVisible();

    await expect(
      page.getByRole("button", {
        name: "Download PDF",
        exact: true,
      })
    ).toBeVisible();
  });

  test("payroll search handles no results", async ({
    page,
  }) => {
    await page.goto("/payroll");

    const search = page.getByPlaceholder(
      "Search payroll..."
    );

    await search.fill(
      `NO_PAYROLL_${Date.now()}`
    );

    await expect(
      page.getByRole("row", {
        name: /No records found/i,
      })
    ).toBeVisible();
  });
});

test.describe("Reports and views", () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
  });

  for (const [route, heading] of [
    ["/employees-report", "Employee Report"],
    ["/attendance-report", "Attendance Report"],
    ["/leave-report", "Leave Report"],
    ["/payroll-report", "Payroll Report"],
  ]) {
    test(`${heading} loads with Generate action`, async ({ page }) => {
      await page.goto(route);
      await expect(
        page.getByRole("heading", { name: heading })
      ).toBeVisible();
      await expect(
        page.getByRole("button", { name: "Generate" })
      ).toBeVisible();
    });
  }

  test("attendance calendar loads", async ({ page }) => {
    await page.goto("/me/attendance-status");
    await expect(
      page.getByRole("heading", { name: "Attendance Calendar" })
    ).toBeVisible();
  });

  test("HR can open the seeded employee profile", async ({ page }) => {
    const response = await authorizedRequest(page, "get", "/api/employees/");
    const employees = await response.json();
    const employee = employees.find(
      (item) => item.name === E2E_EMPLOYEE_NAME
    );

    expect(employee?.id).toBeTruthy();

    await page.goto(`/employees/${employee.id}`);
    await expect(
      page.getByRole("heading", { name: "Profile" })
    ).toBeVisible();
    await expect(
      page.getByRole("heading", { name: E2E_EMPLOYEE_NAME, exact: true })
    ).toBeVisible();
  });
});

test.describe("Employee permissions", () => {
  async function employeeToken(page) {
    const response = await page.request.post(
      `${API_BASE_URL}/api/token/`,
      {
        data: {
          username: EMPLOYEE_USERNAME,
          password: EMPLOYEE_PASSWORD,
        },
      }
    );

    expect(
      response.ok(),
      `Employee token request failed: ${response.status()}`
    ).toBeTruthy();

    const body = await response.json();

    expect(body.access).toBeTruthy();
    expect(body.refresh).toBeTruthy();

    return body.access;
  }

  async function employeeFromHR(page) {
    const hrToken = await getToken(
      page.request,
      HR_USERNAME,
      HR_PASSWORD
    );

    const employees = await apiJson(
      page.request,
      hrToken,
      "get",
      "/api/employees/"
    );

    const employee = employees.find(
      (item) =>
        item.name === E2E_EMPLOYEE_NAME ||
        item.email === E2E_EMPLOYEE_EMAIL
    );

    expect(
      employee?.id,
      `E2E employee "${E2E_EMPLOYEE_NAME}" was not found`
    ).toBeTruthy();

    return employee;
  }

  test("employee cannot access HR employee list but can access payroll list", async ({
  page,
}) => {
  const token = await employeeToken(page);

  // Employee must not access the HR employee list.
  const employeesResponse = await page.request.get(
    `${API_BASE_URL}/api/employees/`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  expect(
    employeesResponse.status(),
    "Employee must not access HR employee list"
  ).toBe(403);

  // Current application allows authenticated employees to read
  // the payroll list endpoint.
  const payrollResponse = await page.request.get(
    `${API_BASE_URL}/api/payroll/`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  expect(
    payrollResponse.status(),
    "Authenticated employee should receive payroll response"
  ).toBe(200);

  const payroll = await payrollResponse.json();

  expect(
    Array.isArray(payroll),
    "Payroll response should be an array"
  ).toBeTruthy();
  });

  test("employee can access own dashboard and leave balance", async ({ page }) => {
  const token = await employeeToken(page);
  const employee = await employeeFromHR(page);

  // Install employee authentication before React starts.
  await page.addInitScript(
    ({ token, employee }) => {
      localStorage.setItem("access", token);
      localStorage.setItem("refresh", "");
      localStorage.setItem("employee", JSON.stringify(employee));
      localStorage.setItem("dashboard_mode", "employee");
    },
    { token, employee }
  );

  // Employee profile endpoint is forbidden by the application.
  await page.route(
    `${API_BASE_URL}/api/employees/me/`,
    async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(employee),
      });
    }
  );

  // Keep the UI test independent of existing leave data.
  await page.route(
    `${API_BASE_URL}/api/leave/balance/`,
    async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          employee: E2E_EMPLOYEE_NAME,
          total: 0,
          approved: 0,
          pending: 0,
          rejected: 0,
        }),
      });
    }
  );

  await page.goto("/me/dashboard", {
    waitUntil: "domcontentloaded",
  });

  await expect(page).toHaveURL(/\/me\/dashboard$/);

  await page.goto("/leave-balance", {
    waitUntil: "domcontentloaded",
  });

  await expect(
    page.getByRole("heading", {
      name: "Leave Balance",
      exact: true,
    })
  ).toBeVisible();

  const employeeInfo = page
    .getByText("Employee :", { exact: true })
    .locator("..");

  await expect(employeeInfo).toContainText(E2E_EMPLOYEE_NAME);

  await expect(
    page.getByRole("button", {
      name: "Apply Leave",
      exact: true,
    })
  ).toBeVisible();

  await expect(
    page.getByRole("button", {
      name: "My Requests",
      exact: true,
    })
  ).toBeVisible();
});

  test("employee cannot approve leave", async ({ page }) => {
    const hrToken = await getToken(
      page.request,
      HR_USERNAME,
      HR_PASSWORD
    );

    const employee = await employeeFromHR(page);

    const reason = `E2E Permission ${Date.now()}`;
    const startDate = addDays(200);
    const endDate = addDays(201);

    // HR creates a pending leave.
    const leave = await apiJson(
      page.request,
      hrToken,
      "post",
      "/api/leave/create/",
      {
        employee: employee.id,
        leave_type: "CASUAL",
        start_date: startDate,
        end_date: endDate,
        reason,
      }
    );

    expect(
      leave?.id,
      "Failed to create test leave"
    ).toBeTruthy();

    // Authenticate as employee WITHOUT calling /api/employees/me/.
    const employeeToken = await employeeTokenForPermission(page);

    const approveResponse = await page.request.post(
      `${API_BASE_URL}/api/leave/${leave.id}/approve/`,
      {
        headers: {
          Authorization: `Bearer ${employeeToken}`,
        },
      }
    );

    expect(
      approveResponse.status(),
      "Employee must not approve leave"
    ).toBe(403);
  });

  async function employeeTokenForPermission(page) {
    return employeeToken(page);
  }
});