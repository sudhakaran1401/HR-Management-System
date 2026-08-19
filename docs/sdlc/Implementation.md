# HR Management System — SDLC Stage 5: Implementation

## 1. Purpose

This document describes how the System Design was implemented in the HR Management System (HRMS).

The project is an **individual academic project**, so all implementation activities were performed by the student/developer.

The implementation uses a full-stack architecture consisting primarily of:

- React frontend
- Django backend
- Django REST Framework APIs
- MySQL database
- JWT authentication
- Docker/Docker Compose
- GitHub Actions CI/CD

---

## 2. Implementation Overview

The implementation follows the design developed in the previous SDLC stages:

```text
React Frontend
      |
      | REST API
      v
Django / Django REST Framework
      |
      v
MySQL Database
```

The application is divided into functional modules so that HR operations can be developed and maintained independently.

---

## 3. Development Environment

The implementation requires the project's configured development environment, including:

- Python
- Django
- Django REST Framework
- Node.js
- React
- MySQL
- Git
- Docker / Docker Compose
- Browser-based development/testing tools

Environment-specific values such as credentials and secrets should be stored through environment configuration rather than hard-coded in source code.

---

## 4. Backend Implementation

The Django backend implements the server-side application logic and REST APIs.

The major backend areas include:

```text
backend/
|
+-- accounts/
+-- employees/
+-- attendance/
+-- leave/
+-- payroll/
+-- dashboard/
+-- reports/
+-- project configuration
```

### 4.1 Accounts

The accounts functionality provides:

- User authentication
- JWT-based authentication
- User-related operations
- Permission/role handling
- Protected API access

### 4.2 Employees

The employee module implements:

- Employee records
- Employee profile information
- Employee CRUD operations
- Employee-related validation
- API endpoints for employee management

### 4.3 Attendance

The attendance module implements:

- Attendance records
- Attendance creation/update operations
- Attendance retrieval
- Attendance validation
- Attendance-related API operations
- Calendar/report functionality where supported

### 4.4 Leave

The leave module implements:

- Leave requests
- Leave types
- Leave status
- Leave approval/rejection
- Leave balance
- Leave validation
- Leave history
- Leave-related API operations

### 4.5 Payroll

The payroll module implements:

- Salary information
- Payroll records
- Payroll calculations
- Deductions
- Gross/net salary calculations
- Payroll history
- Payslip/report functionality where supported

### 4.6 Dashboard

The dashboard functionality provides aggregated HR information for relevant users.

It connects application data to dashboard statistics and visual information.

### 4.7 Reports

The reporting functionality supports reporting and export operations for HR information where implemented.

---

## 5. Database Implementation

The application uses a relational database for persistent HR information.

The major data areas are:

```text
Users
  |
Employees
  |
  +---- Attendance
  +---- Leave
  |        |
  |        +---- Leave Balance
  |
  +---- Payroll / Salary
```

Database models define the application's persistent entities and their relationships.

Validation and model/database constraints are used for important integrity requirements such as uniqueness and valid relationships.

---

## 6. Frontend Implementation

The React frontend provides the user-facing HRMS application.

Major frontend areas include:

- Login/authentication
- Dashboard
- Employee management
- Attendance
- Leave
- Payroll
- Reports
- Profile
- Shared UI components
- API services
- Hooks/utilities

The frontend communicates with the backend through REST APIs.

### Frontend Responsibilities

The frontend handles:

- User interaction
- Form submission
- Displaying API data
- Navigation
- Loading states
- Error messages
- Search/filtering
- Tables
- Charts
- Responsive layouts

Backend authorization remains responsible for enforcing access permissions.

---

## 7. API Implementation

The Django REST Framework provides the communication layer between frontend and backend.

Conceptually:

```text
React Component
      |
      v
API Service
      |
      v
REST Endpoint
      |
      v
Serializer / Validation
      |
      v
Business Logic
      |
      v
Database
      |
      v
API Response
      |
      v
React Component
```

API operations support the main HR resources, including:

- Authentication
- Employees
- Attendance
- Leave
- Payroll
- Dashboard
- Reports

---

## 8. Authentication and Authorization Implementation

JWT-based authentication is used for protected API access.

The implementation distinguishes authenticated access from unauthenticated access.

Role/permission checks protect administrative functionality.

The backend is treated as the authoritative security layer, meaning frontend route/menu restrictions are not relied upon as the only access-control mechanism.

---

## 9. Validation and Business Logic Implementation

Business rules are implemented through a combination of:

- Model validation
- Serializer/API validation
- Application/business logic
- Database constraints

Examples include:

- Employee uniqueness rules
- Attendance uniqueness
- Leave date validation
- Leave overlap validation
- Leave status handling
- Payroll period uniqueness
- Payroll calculations
- Role-based access

This prevents invalid operations from being accepted by the application.

---

## 10. Import and Export Implementation

The project includes data import mechanisms for supported HR datasets, including management commands for areas such as:

- Employees
- Attendance
- Leave
- Salary

The application also provides report/export functionality where implemented.

The general import process is:

```text
Input File
    |
    v
Read Data
    |
    v
Validate
    |
    v
Transform
    |
    v
Save
    |
    v
Import Result
```

---

## 11. Testing Implementation

Testing is implemented at multiple levels.

The existing project contains:

- Backend unit tests
- Integration tests
- Security tests
- System tests
- Acceptance tests
- Regression tests
- Reliability tests
- Recovery tests
- Frontend tests
- Playwright end-to-end tests
- Accessibility tests using Axe/Playwright
- Locust performance/load tests

Testing is therefore integrated into implementation rather than postponed until the end of development.

---

## 12. Deployment Implementation

The project includes containerization and deployment configuration.

Docker/Docker Compose are used to make the application environment reproducible.

The deployment structure conceptually separates:

```text
Frontend
   |
Backend
   |
Database
```

The exact services and configuration are defined by the project's Docker and deployment files.

---

## 13. CI/CD Implementation

GitHub Actions is used to automate quality checks.

The CI process includes checks such as:

- Backend tests
- System/functional tests
- Frontend tests
- Linting
- Frontend build
- End-to-end tests

This allows code changes to be checked automatically before being treated as release-ready.

---

## 14. Implementation Workflow

As an individual developer, the implementation process follows:

```text
Requirement
    |
    v
Design
    |
    v
Implement Backend
    |
    v
Implement Frontend
    |
    v
Integrate API + Database
    |
    v
Run Tests
    |
    +--> Failure --> Debug/Fix --> Re-test
    |
    v
Build/Deploy
```

Version control is used to track implementation changes.

---

## 15. Implementation Standards

The implementation should maintain:

- Clear module separation
- Meaningful naming
- Reusable components
- Input validation
- Secure configuration
- Error handling
- Automated tests
- Version control
- Documentation of important configuration

Because this is an individual project, simplicity and maintainability are prioritized over unnecessary architectural complexity.

---

## 16. Implementation Status

| Area | Status |
|---|---|
| React frontend | Implemented |
| Django backend | Implemented |
| REST APIs | Implemented |
| Authentication | Implemented |
| Authorization | Implemented |
| Employee management | Implemented |
| Attendance | Implemented |
| Leave | Implemented |
| Payroll | Implemented |
| Dashboard | Implemented |
| Reports | Implemented |
| Database | Implemented |
| Import functionality | Implemented |
| Automated testing | Implemented |
| E2E testing | Implemented |
| Accessibility testing | Implemented |
| Performance testing | Implemented |
| Docker | Implemented |
| CI/CD | Implemented |

---

## 17. Implementation Gaps

The implementation is substantially complete, but the following areas can be improved as part of future maintenance:

- More explicit API documentation
- More detailed production configuration documentation
- Formal audit logging if required
- Formal backup/restore operational procedures
- Additional security hardening
- More explicit configuration documentation
- Formal code-quality and contribution guidelines

These are improvements rather than evidence that the core application has not been implemented.

---

## 18. Implementation Conclusion

The HRMS design has been translated into a working full-stack application.

The implementation provides the main HR modules, frontend/backend integration, database persistence, authentication, authorization, reporting, automated testing, containerization, and CI/CD.

### Implementation Status

**Status: Implemented**

The next SDLC stage is **Testing**, where the implemented system and its existing test suites will be documented in detail.
