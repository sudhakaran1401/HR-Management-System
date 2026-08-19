# HR Management System — SDLC Stage 2: Requirements Analysis

## 1. Purpose

This document defines the functional and non-functional requirements for the HR Management System (HRMS).

The requirements are based on the functionality actually present in the existing project, including the backend APIs, frontend application, database models, authentication, reporting, testing and deployment configuration.

Because this is an **individual academic project**, the requirements are defined at a level that is realistic for one developer to implement, test and maintain.

---

## 2. Project Goal

The HRMS will provide a centralized web-based platform for managing employee information and core HR operations, including attendance, leave, payroll, dashboards, reports and employee self-service.

---

## 3. User Roles

The system will support the following primary user roles:

### 3.1 HR/Admin

HR/Admin users will be able to manage organizational HR information and perform administrative HR operations.

### 3.2 Employee

Employees will be able to access their own HR information and employee self-service functions.

### 3.3 System Administrator

Where applicable, system administration will include management of users, permissions and application configuration.

---

# 4. Functional Requirements

## FR-01 — User Authentication

The system will allow authorized users to log in using valid credentials.

The system will:

- Authenticate users securely.
- Issue JWT access/refresh tokens where configured.
- Protect authenticated API resources.
- Allow users to log out.
- Prevent unauthenticated users from accessing protected functionality.

**Current implementation status:** Implemented.

---

## FR-02 — Role-Based Authorization

The system will restrict functionality according to the user's role.

The system will:

- Distinguish HR/Admin access from employee access.
- Protect HR-only operations.
- Prevent employees from accessing unauthorized employee records or administrative operations.
- Protect backend APIs as well as frontend routes.

**Current implementation status:** Implemented.

---

## FR-03 — Employee Management

HR/Admin users will be able to manage employee records.

The system will support:

- Creating/Viewing/Updating/Deleting employee records.
- Searching/filtering employee records.
- Viewing/Updating employee profiles.
- Associating employee records with user accounts.
- Managing employee information such as name, email, phone number etc supported.
- Generate/Export Employee reports

**Current implementation status:** Implemented.

---

## FR-04 — Employee Self-Service Profile

Employees will be able to access their own profile information.

The system will:

- Display the logged-in employee's profile.
- Prevent access to unrelated employees' private profile information.

**Current implementation status:** Implemented.

---

## FR-05 — Attendance Management

The system will support employee attendance management.

HR/Admin users will be able to:

- Create/View attendance records.
- Mark/View daily attendance for an employee in case of backup.
- Search/filter attendance records.
- Generate/Export attendance reports.

Employees will be able to:

- Mark/View daily attendance where permitted.
- View attendance calendar information.

The system will prevent duplicate attendance records for the same employee and date.

**Current implementation status:** Implemented.

---

## FR-06 — Leave Management

Employees will be able to:

- Submit/View leave requests.
- Track request status.
- View leave history.
- View leave balance.
- Update eligible requests.

HR/Admin users will be able to:

- View/Approve/Reject leave requests.
- View leave history.
- View leave balances.
- Generate/Export leave reports.

The system will validate leave dates.

The system will prevent invalid date ranges where the start date is after the end date.

The system will detect overlapping leave requests for the same employee.

**Current implementation status:** Implemented.

---

## FR-07 — Leave Balance

The system will maintain leave balances for employees.

The system will support leave categories including:

- Sick leave
- Casual leave
- Annual leave

The system will allow authorized users to view the available leave balance.

**Current implementation status:** Implemented.

---

## FR-08 — Payroll Management

HR/Admin users will be able to:

- Create/View/Update payroll records.
- Search/filter payroll information.
- Generate/Export payroll reports.
- Generate/download payslips.

Employees will be able to:

- View their payroll history.
- View/Downloads payslip information.

The payroll system will calculate:

- Basic salary
- HRA
- Allowances
- Gross salary
- PF
- Tax
- Other deductions
- Total deductions
- Net pay

The system will maintain salary information by employee and pay month.

The system will prevent duplicate salary records for the same employee and pay month.

**Current implementation status:** Implemented.

---

## FR-09 — Dashboard

The system will provide role-appropriate dashboards.

### HR Dashboard

The dashboard will provide information such as:

- Employee statistics
- Attendance summary
- Leave summary
- Payroll summary
- KPI information
- Charts/visual summaries
- Access to reports

### Employee Dashboard

The dashboard will provide information such as:

- Attendance overview
- Leave overview
- Payroll overview
- Profile information

### Leave Dashboard

The dashboard will provide leave information for specific employee such as:

- Applied/Approved/Rejected/Pending Leave requests summary 
- Sick/Casual/Annual leave days summary 

**Current implementation status:** Implemented.

---

## FR-10 — Reports and Data Export

The system will provide reporting functionality for major HR modules.

Reports will support, where implemented:

- Filtering Employee/Attendance/Leave/Payroll reports
- Summary information
- Chart-based visualization
- CSV/Excel data export where supported
- PDF/report downloads where supported

**Current implementation status:** Implemented.

---

## FR-11 — Bulk Data Import

The system will support bulk import of HR data through supported import mechanisms.

The current project provides management commands for:

- Employee import
- Attendance import
- Leave import
- Salary import

The import process will validate data sufficiently to avoid corrupting application records.

**Current implementation status:** Implemented.

---

## FR-12 — Calendar

Emeployee Attendance calendar for specific employee.

**Current implementation status:** Implemented.

---

## FR-13 — Search, Filtering and Pagination

The system will provide search/filtering capabilities for major list-based HR records where supported.

The frontend will support pagination where applicable.

**Current implementation status:** Implemented.

---

## FR-14 — User Interface

The system will provide a responsive web interface.

The interface will support:

- Responsive layouts
- Reusable React components
- Loading states
- Alerts/error messages
- Search
- Pagination
- Charts
- Navigation
- Dark theme
- Mobile-friendly layouts

**Current implementation status:** Implemented.

---

## FR-15 — API Services

The backend will expose REST API endpoints for the major application modules.

The APIs will support appropriate operations for:

- Authentication/current user
- Employees
- Attendance
- Leave
- Payroll
- Dashboards

The API will enforce authentication and authorization rules.

**Current implementation status:** Implemented.

---

# 5. Non-Functional Requirements

## NFR-01 — Security

The system will protect sensitive HR information.

The system will:

- Authenticate users.
- Authorize protected operations.
- Protect sensitive API endpoints.
- Prevent unauthorized access to employee data.
- Use secure token-based authentication where configured.
- Validate user input.
- Apply appropriate security controls to administrative operations.

**Current status:** Partially/strongly implemented; security testing is also present.

---

## NFR-02 — Performance

The system should provide acceptable response times for normal HR operations.

The system should remain usable as the number of users and records increases.

Performance will be evaluated using load/performance testing.

**Current status:** Performance testing is implemented.

---

## NFR-03 — Reliability

The system should continue operating correctly when valid operations are performed repeatedly.

Failures should be handled without unnecessary data corruption.

**Current status:** Reliability and recovery tests are present.

---

## NFR-04 — Availability

The deployed application should be available to authorized users during its intended operating period.

Deployment configuration should support reliable application startup and recovery.

**Current status:** Deployment infrastructure exists; formal availability targets are not yet defined.

---

## NFR-05 — Maintainability

The system should be organized into separate application modules so that individual functionality can be modified without unnecessarily affecting unrelated functionality.

The project should maintain automated regression tests to identify unintended changes.

**Current status:** Good foundation through modular structure and regression testing; a formal maintenance policy is still required.

---

## NFR-06 — Usability

The system should provide an understandable interface for HR/Admin users and employees.

The interface should:

- Clearly identify available functions.
- Provide useful validation/error messages.
- Provide loading feedback.
- Use consistent navigation.
- Support responsive layouts.

**Current status:** Implemented.

---

## NFR-07 — Accessibility

The application should be usable by people with different accessibility needs.

Accessibility checks should be included in browser-based testing.

**Current status:** Accessibility testing using Axe/Playwright is present.

---

## NFR-08 — Scalability

The system should be designed so that additional employees, attendance records, leave records and payroll records can be added without redesigning the complete application.

Database indexing and appropriate API/query design should be used where necessary.

**Current status:** Partially addressed; formal scalability targets are not defined.

---

## NFR-09 — Data Integrity

The system will maintain consistent HR data.

Examples include:

- Unique employee email addresses.
- One attendance record per employee with specific date.
- Valid leave date ranges.
- No overlapping leave requests where validation applies.
- One salary record per employee/pay month.
- Correct relationships between users and employees.

**Current status:** Implemented through model constraints and validation.

---

## NFR-10 — Backup and Recovery

The system should have a documented method for backing up important database/application data and recovering from failures.

**Current status:** Recovery testing exists, but a complete operational backup policy is not yet documented.

---

## NFR-11 — Compatibility

The frontend should operate correctly in supported modern browsers.

The application should support the configured desktop and mobile-responsive layouts.

**Current status:** Browser/E2E testing is present; a formal supported-browser matrix should be documented.

---

# 6. Data Requirements

The system requires data for the following major entities:

- User
- Employee
- Employee Profile
- Attendance
- Leave Request
- Leave Balance
- Salary/Payroll History

The database will maintain appropriate relationships between these entities.

Test/development data may be generated or imported from the project's supported sample Excel files.

Sensitive real employee information should not be used for development/testing without appropriate authorization and protection.

---

# 7. Business Rules

The following business rules are identified from the current implementation.

### BR-01 — Employee Email

Employee email addresses will be unique.

### BR-02 — Attendance Uniqueness

An employee will have at most one attendance record for a specific date.

### BR-03 — Leave Date Validation

A leave request will not have a start date later than its end date.

### BR-04 — Leave Overlap

An employee should not have overlapping leave requests.

### BR-05 — Leave Status

Leave requests will use defined statuses such as:

- Pending
- Approved
- Rejected

### BR-06 — Leave Types

The current implementation supports:

- Sick Leave
- Casual Leave
- Annual Leave

### BR-07 — Payroll Uniqueness

An employee will have at most one salary/payroll history record for a given pay month.

### BR-08 — Payroll Calculation

Payroll calculations will derive gross salary, deductions and net pay according to the business rules implemented by the payroll module.

### BR-09 — Role Access

Administrative HR functions will not be available to ordinary employees unless explicitly permitted.

---

# 8. External Interfaces

## 8.1 User Interface

The main user interface is a React web application.

## 8.2 API Interface

The frontend communicates with the Django REST Framework backend through HTTP APIs.

## 8.3 Database Interface

The backend communicates with the MySQL database.

## 8.4 File Interface

The system supports Excel-based import and CSV/PDF/report-related export functionality where implemented.

---

# 9. Requirement Traceability

The following table connects major requirements to the existing implementation.

| Requirement Area | Existing Evidence |
|---|---|
| Authentication | `accounts` application, JWT configuration, authentication APIs |
| Authorization | Protected views/APIs and role-based access logic |
| Employee Management | `employees` application and REST APIs |
| Attendance | `attendance` application, model, services and REST APIs |
| Leave | `leave` application, validation, balance and REST APIs |
| Payroll | `payroll` application, salary model and REST APIs |
| Dashboards | `dashboard` application and dashboard APIs |
| Reports | CSV/PDF/report API endpoints and reporting libraries |
| Bulk Import | Django management commands and Excel sample data |
| Frontend | React pages/components/services |
| E2E | Playwright test suite |
| Accessibility | Axe/Playwright testing |
| Performance | Locust testing |
| CI/CD | GitHub Actions workflows |
| Containerization | Docker/Docker Compose configuration |

---

# 10. Requirements Currently Missing or Needing Formal Definition

Although many functional requirements are already implemented, the following requirements should be formally defined before considering the Requirements Analysis stage complete.

## 10.1 Formal Service-Level Targets

Specific targets should be defined for:

- API response time
- Page load time
- Concurrent users
- Maximum supported dataset/record size
- Availability

## 10.2 Formal Browser Support Matrix

The project should document exactly which browser versions are officially supported.

## 10.3 Backup Requirements

A formal requirement should define:

- Backup frequency
- Backup retention
- Recovery Point Objective (RPO)
- Recovery Time Objective (RTO)

## 10.4 Security Requirements

A more detailed security specification should define:

- Password policy
- Token expiry requirements
- Session/token revocation behavior
- Rate limiting
- Audit logging
- Security headers
- Sensitive-data handling
- Production secret management

## 10.5 Payroll Business Rules

Payroll rules should be formally specified rather than existing only in implementation code.

For example:

- Salary calculation rules
- Leave deduction rules
- PF rules
- Tax rules
- Allowance rules
- Rounding rules
- Finalization/locking rules

## 10.6 Audit Requirements

The project should define whether changes to sensitive records must be audited, including:

- Who changed a record
- What was changed
- When it was changed
- Previous/new values where required

## 10.7 Data Retention

The project should define how long employee, attendance, leave and payroll records should be retained.

---

# 11. Requirements Analysis Status

### Implemented Requirements

Most core functional requirements are already represented in the existing HRMS application.

### Documentation Gap

The major gap is that these requirements were not previously consolidated into a formal SDLC Requirements Analysis document.

### Remaining Requirement Work

Before moving to System Analysis, the project should finalize:

- Formal non-functional targets
- Security requirements
- Backup/recovery requirements
- Payroll business rules
- Audit requirements
- Data-retention requirements
- Browser/support requirements
- Strict Attendance marking (current timestamp marking) / Update attendance

**Requirements Analysis Stage: Substantially completed, with the above items requiring formal definition.**

**Next SDLC Stage: System Analysis**
