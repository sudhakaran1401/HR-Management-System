# HR Management System — SDLC Stage 3: System Analysis

## 1. Purpose

This document defines the System Analysis stage for the HR Management System (HRMS).

The purpose of this stage is to analyze how the identified requirements are transformed into users, workflows, data, business rules, system interactions, and functional boundaries before detailed system design.

This analysis is based on the existing HRMS implementation and the requirements documented in `02-requirements.md`.

---

## 2. System Context

The HRMS is a centralized web application through which HR/Admin users and employees interact with HR-related services.

```text
HR/Admin / Employee
        |
        v
 React Web Application
        |
        v
 Django REST API
        |
        v
 Authentication / Business Logic
        |
        v
 MySQL Database
```

The system also interacts with supporting infrastructure for JWT authentication, report generation, file import/export, automated testing, Docker, and CI/CD.

---

## 3. Actors

### 3.1 Employee

The Employee is an authenticated user who primarily accesses personal HR information.

Main activities:

- Login
- View profile
- View attendance
- Mark attendance where permitted
- Submit leave
- View leave status/history
- View leave balance
- View payroll
- Download/view payslips
- View dashboard summaries

### 3.2 HR/Admin

HR/Admin users manage organizational HR operations.

Main activities:

- Login
- Manage Employees/Attendances/Leaverequests/Payroll
- View dashboards
- Generate/Export reports
- Import Data

### 3.3 System Administrator

Where applicable, the administrator manages system-level users, roles and access.

### 3.4 Project Developer

Because this is an individual academic project, the student/developer performs the analysis, design, implementation, testing, deployment and maintenance activities.

The developer is not a normal business user of the system; this role represents project responsibility.

---

## 4. Functional Decomposition

```text
HR Management System
|
+-- Authentication & Authorization
|
+-- Employee Management
|   +-- Create/Read/Update/Delete Employee records
|   +-- Employee profiles 
|
+-- Attendance Management
|   +-- Record/View attendance
|   +-- Attendance calendar
|
+-- Leave Management
|   +-- Apply/Update/View leaverequests
|   +-- Review/Approve/reject leave
|   +-- View Leave balance
|
+-- Payroll Management
|   +-- Create/View/Update Salary records
|   +-- Download Payslips
|
+-- Dashboard
|   +-- HR dashboard
|   +-- Employee dashboard
|   +-- Leave request dashboard
|
+-- Reports
    +-- Generate/Export Employee reports
    +-- Generate/Export Attendance reports
    +-- Generate/Export Leave reports
    +-- Generate/Export Payroll reports
```

---

## 5. Major User Workflows

### 5.1 Authentication

```text
User
  |
  v
Enter Credentials
  |
  v
Backend Authentication
  |
  +-- Invalid --> Error Response
  |
  +-- Valid
       |
       v
     JWT Token
       |
       v
Access Protected Resources
```

### 5.2 Employee Management

```text
HR/Admin
   |
   v
Employee Management
   |
   +--> Create
   +--> View
   +--> Update
   +--> Delete/Manage
   |
   v
Validation
   |
   v
Database
   |
   v
Success/Error Response
```

### 5.3 Attendance

```text
Employee / HR
      |
      v
Attendance Request
      |
      v
Validate Employee + Date
      |
      +--> Duplicate/Invalid --> Error
      |
      v
Create/Update Attendance
      |
      v
Database
      |
      v
Attendance Result
```

### 5.4 Leave

```text
Employee
   |
   v
Submit Leave
   |
   v
Validate Dates + Overlap + Balance
   |
   +--> Invalid --> Error
   |
   v
Pending -> Update if needed
   |
   v
HR/Admin Review
   |
   +--> Reject
   |
   +--> Approve
          |
          v
      Updated  Leave Status/Balance
```

### 5.5 Payroll

```text
Employee Information
       |
       v
Salary Information
       |
       v
Payroll Calculation
       |
       +--> Gross Salary
       +--> Allowances
       +--> Deductions
       +--> PF/Tax where applicable
       |
       v
Net Pay
       |
       v
Payroll Record
       |
       v
Payslip / Report
```

---

## 6. Data Analysis

The main business data can be grouped into:

- User
- Employee
- Attendance
- Leave Request
- Leave Balance
- Payroll/Salary

### User

Represents an authenticated application user. A user may be associated with an employee and has an applicable role/permission level.

### Employee

Represents an employee managed by HR. An employee can have attendance records, leave requests, leave balances and payroll/salary records.

### Attendance

Represents an employee's attendance for a date. An employee should not have duplicate attendance for the same date.

### Leave

Represents an employee leave request. Important data includes employee, leave type, start date, end date and status.

### Leave Balance

Represents the available leave allocation for an employee.

### Payroll/Salary

Represents salary/payroll information for an employee and pay period. Duplicate payroll records for the same employee/pay month should be prevented.

---

## 7. Entity Relationships

The conceptual relationship structure is:

```text
User
 |
 | 1 : 0..1
 v
Employee
 |
 +------------------+
 |        |         |
 v        v         v
Attendance Leave   Payroll
            |
            v
       Leave Balance
```

The exact database relationship and field definitions should be documented in the System Design stage.

---

## 8. Business Rule Analysis

### BR-01 — Authentication

Protected functions require an authenticated user.

### BR-02 — Authorization

Users can only perform operations permitted by their role.

### BR-03 — Employee Uniqueness

Employee email information should satisfy the configured uniqueness constraints.

### BR-04 — Attendance Uniqueness

An employee should have one attendance record per applicable date.

### BR-05 — Leave Date Validity

A leave request cannot have an end date before its start date.

### BR-06 — Leave Overlap

Overlapping leave requests for the same employee should be detected/prevented.

### BR-07 — Leave Status

Leave requests use defined statuses such as Pending, Approved and Rejected.

### BR-08 — Leave Balance

Approved leave affects the employee's applicable leave balance according to the implemented rules.

### BR-09 — Payroll Period Uniqueness

An employee should not have duplicate payroll/salary records for the same pay period.

### BR-10 — Payroll Calculation

Gross salary, deductions and net pay must follow the payroll calculation rules implemented by the system.

---

## 9. Input Analysis

The system receives input through:

- Login credentials
- Employee details
- Attendance actions
- Leave requests
- Payroll information
- Search/filter parameters
- Supported employee, attendance, leave and salary import files
- Frontend REST API requests

All input should be validated before being used to modify business data.

---

## 10. Output Analysis

The system produces:

- Web pages
- API responses
- Success/error messages
- Employee information
- Attendance information
- Leave status and balances
- Payroll information
- Payslips
- Dashboards
- Reports
- Export files

Outputs should be restricted according to the authenticated user's permissions.

---

## 11. Error and Exception Analysis

The system must account for:

### Authentication Errors

- Invalid credentials
- Missing authentication
- Invalid/expired token

### Employee Errors

- Duplicate employee information
- Invalid employee data
- Employee not found

### Attendance Errors

- Duplicate attendance
- Invalid employee
- Invalid date/data

### Leave Errors

- Invalid date range
- Overlapping leave
- Invalid leave balance where applicable
- Leave record not found

### Payroll Errors

- Invalid salary data
- Duplicate payroll period
- Employee not found
- Invalid payroll input

### API/System Errors

- Invalid request
- Unauthorized request
- Resource not found
- Server-side failure

---

## 12. Security Analysis

The system handles sensitive employee and payroll information.

The analysis therefore identifies these security needs:

- Authentication
- Role-based authorization
- Protected API endpoints
- Input validation
- Controlled access to employee records
- Secure authentication-token handling
- Protection of secrets/configuration

The existing project also contains security-focused automated tests.

Further security requirements such as rate limiting, audit logging, password policy and production security controls should be finalized during System Design.

---

## 13. Performance Analysis

Performance-sensitive areas include:

- Employee listing/search
- Attendance queries
- Leave queries
- Payroll queries
- Dashboard aggregation
- Report generation
- Data import/export

The existing project includes performance/load testing. Formal response-time and concurrency targets should be defined in the Design/Testing documentation.

---

## 14. Integration Analysis

The main system interaction is:

```text
React Frontend
      |
      | HTTP/REST
      v
Django REST Framework
      |
      +--> Authentication
      +--> Business Logic
      +--> Reporting
      |
      v
MySQL Database
```

Supporting integrations include Docker, GitHub Actions/CI, Playwright, Locust, and report/file processing.

The System Design stage should define the exact API endpoints, request/response formats, database interfaces and deployment connections.

---

## 15. Current System vs Requirements

| Area | Analysis Result |
|---|---|
| Authentication | Implemented |
| Authorization | Implemented |
| Employee management | Implemented |
| Attendance | Implemented |
| Leave | Implemented |
| Leave balance | Implemented |
| Payroll | Implemented |
| Dashboard | Implemented |
| Reports | Implemented |
| Import/export | Implemented |
| Frontend/backend integration | Implemented |
| Automated testing | Implemented |
| E2E testing | Implemented |
| Accessibility testing | Implemented |
| Performance testing | Implemented |
| Formal audit analysis | Needs further definition |
| Formal backup/retention analysis | Needs further definition |
| Formal performance targets | Needs further definition |

---

## 16. Missing Analysis Artifacts

The existing implementation provides the system behavior, but the following formal analysis artifacts should be documented:

### 16.1 Use Case Diagram

Should show:

- Employee
- HR/Admin
- System Administrator
- Major system functions

### 16.2 Use Case Specifications

Each major use case should define:

- Actor
- Preconditions
- Main flow
- Alternative flow
- Exceptions
- Postconditions

### 16.3 Data Flow Diagram

Should show how employee, attendance, leave and payroll data move through the system.

### 16.4 Data Dictionary

Should document:

- Entity
- Field
- Data type
- Required/optional status
- Validation
- Description

### 16.5 Business Rule Catalogue

Payroll, leave and authorization rules should be documented independently from source code.

---

## 17. System Analysis Conclusion

The HRMS is a multi-module application with defined users, workflows, data relationships, business rules, security requirements and system interactions.

The major gap is formal documentation of analysis artifacts, rather than absence of system functionality.

### System Analysis Status

**Completed at the conceptual level.**

The next SDLC stage is **System Design**, where this analysis will be converted into formal architecture, database design, API design, component design and UI/navigation design.
