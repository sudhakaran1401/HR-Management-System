# HR Management System — SDLC Stage 4: System Design

## 1. Purpose

This document defines the System Design stage for the HR Management System (HRMS). It converts the requirements and system analysis into a technical design covering architecture, application layers, database structure, APIs, authentication, authorization, frontend, backend, validation, security, testing, and deployment.

This is an individual academic project, so the design is intended to remain practical, maintainable, and achievable by one developer.

## 2. Design Goals

The system design shall:

1. Separate frontend, backend, and database responsibilities.
2. Provide secure access to HR information.
3. Keep major HR modules logically separated.
4. Provide reusable APIs and frontend services.
5. Maintain data integrity through validation and constraints.
6. Support automated testing.
7. Support containerized deployment and CI/CD.
8. Allow future extensions without redesigning the complete system.
9. Remain understandable and maintainable for an individual developer.

## 3. High-Level Architecture

```text
+--------------------------------------------------+
|                React Frontend                    |
| Login | Dashboard | Employees | Attendance       |
| Leave | Payroll | Reports | Profile              |
+------------------------+-------------------------+
                         |
                     HTTP / REST
                         |
                         v
+--------------------------------------------------+
|          Django / Django REST Framework          |
| Authentication | Authorization | Business Logic |
| Employees | Attendance | Leave | Payroll        |
| Dashboard | Reports | Validation                |
+------------------------+-------------------------+
                         |
                         v
+--------------------------------------------------+
|                    MySQL                         |
| Users | Employees | Attendance | Leave | Payroll|
+--------------------------------------------------+
```

Supporting infrastructure includes Docker/Docker Compose, GitHub Actions/CI, Playwright, Locust, and report/file-processing components.

## 4. Architectural Layers

### 4.1 Presentation Layer

The React frontend is responsible for:

- User interface
- Navigation
- Forms
- Tables
- Dashboards
- Charts
- API communication
- Loading and error states
- Responsive layouts
- Client-side validation where appropriate

The frontend does not directly access the database.

### 4.2 Application/API Layer

Django and Django REST Framework are responsible for:

- Authentication
- Authorization
- Request validation
- Business rules
- CRUD operations
- Serialization
- Reporting operations
- Communication with the database

### 4.3 Data Layer

The database is responsible for persistent HR data, relationships, integrity constraints, and queries.

## 5. Backend Module Design

The backend is logically divided into HR-related modules:

```text
backend/
|
+-- accounts/
|   +-- Authentication
|   +-- Users
|   +-- Permissions
|
+-- employees/
|   +-- Employee records
|   +-- Employee profiles
|
+-- attendance/
|   +-- Attendance records
|
+-- leave/
|   +-- Leave requests
|   +-- Leave balances
|   +-- Leave validation
|
+-- payroll/
|   +-- Salary/payroll records
|   +-- Payroll calculations
|
+-- dashboard/
|   +-- Dashboard statistics
|
+-- reports/
|   +-- Reports and exports
|
+-- project configuration
    +-- Settings
    +-- URLs
    +-- API configuration
```

Each module should keep its relevant models, API logic, validation, and tests organized within its functional boundary.

## 6. Frontend Design

The React application is organized conceptually around:

```text
React Application
|
+-- Authentication
+-- Layout / Navigation
+-- Dashboard
+-- Employees
+-- Attendance
+-- Leave
+-- Payroll
+-- Reports
+-- Profile
+-- Shared Components
+-- API Services
+-- Hooks / Utilities
```

The frontend displays data returned by APIs and collects user input. Backend authorization remains the authoritative security control.

## 7. Authentication Design

The system uses token-based authentication.

```text
User
 |
 v
Login Form
 |
 v
Authentication API
 |
 +-- Invalid --> Error
 |
 +-- Valid --> JWT Token
                  |
                  v
          Authenticated Requests
```

Protected backend endpoints must verify authentication before allowing access.

## 8. Authorization Design

Authorization is role-based.

```text
Authenticated User
       |
       +------------------+
       |                  |
    HR/Admin           Employee
       |                  |
       v                  v
Administrative       Personal HR
HR Operations        Operations
```

HR/Admin functionality may include employee management, attendance management, leave approval, payroll, reports, and dashboards.

Employees may access their own profile, attendance, leave, leave balance, payroll, and payslips as permitted.

The backend must enforce permissions independently of frontend navigation.

## 9. Database Design

The conceptual data relationship is:

```text
User
 |
 | 1 : 0..1
 v
Employee
 |
 +----------------------+
 |          |           |
 v          v           v
Attendance  Leave     Payroll
              |
              v
        Leave Balance
```

### Main entities

- **User** — authentication and user access information.
- **Employee** — employee information.
- **Attendance** — attendance records associated with employees and dates.
- **Leave** — leave requests, types, dates, and status.
- **Leave Balance** — employee leave allocations/balances.
- **Payroll/Salary** — salary information for applicable pay periods.

The exact field-level schema should follow the models implemented in the repository.

## 10. Database Integrity

Important integrity rules include:

- Employee email uniqueness where configured.
- One attendance record per employee/date where configured.
- Valid leave date ranges.
- Detection/prevention of overlapping leave.
- Valid leave statuses.
- Prevention of duplicate payroll records for an employee/pay period where configured.

Validation and database/model constraints should work together.

## 11. API Design

The frontend communicates with Django through REST APIs.

Conceptual API groups are:

```text
/api/
|
+-- authentication/
+-- employees/
+-- attendance/
+-- leave/
+-- payroll/
+-- dashboard/
+-- reports/
```

Typical REST operations are:

| Operation | HTTP Method | Purpose |
|---|---|---|
| Create | POST | Create a resource |
| Retrieve | GET | Retrieve resources |
| Update | PUT/PATCH | Update a resource |
| Delete | DELETE | Delete a resource |

Exact endpoint paths should be taken from the implemented URL configuration rather than invented in this document.

## 12. API Request Flow

```text
React Component
      |
      v
Frontend API Service
      |
      v
HTTP Request + JWT
      |
      v
Django REST API
      |
      v
Validation / Business Logic
      |
      v
Database
      |
      v
Serialized Response
      |
      v
React UI
```

APIs should return appropriate HTTP status codes and structured error information.

## 13. Validation Design

Validation occurs at three levels:

### Frontend

Provides immediate user feedback for obvious input errors.

### Backend

The backend is the authoritative validation layer for:

- Required fields
- Data types
- Dates
- Unique values
- Business rules
- Permissions

### Database

Critical integrity constraints should also be enforced at the model/database level where appropriate.

## 14. Error Handling Design

The system should handle:

### Client errors

- Invalid input
- Missing fields
- Unauthorized access
- Resource not found
- Duplicate records

### Server errors

- Unexpected application errors
- Database failures
- Other service failures

The frontend should show understandable error messages without exposing sensitive internal details.

## 15. Security Design

The system handles sensitive employee and payroll information.

The design includes:

- JWT authentication
- Role-based authorization
- Protected API endpoints
- Backend permission enforcement
- Input validation
- Database constraints
- Secure configuration/secrets handling

Additional production-hardening areas should be considered:

- Rate limiting
- Security headers
- Audit logging
- Password policy
- Token lifecycle/revocation
- Secret management
- Dependency security scanning

## 16. Reporting and Export Design

Conceptual reporting flow:

```text
User
 |
 v
Select Report + Filters
 |
 v
Report API
 |
 v
Query / Aggregate HR Data
 |
 v
Generate Report
 |
 +--> Display
 +--> CSV/Excel where supported
 +--> PDF where supported
```

Reports must respect user permissions.

## 17. Import Design

The project supports management-command-based data import.

```text
Import File
    |
    v
Read Data
    |
    v
Validate Records
    |
    +--> Invalid --> Report Errors
    |
    v
Transform / Prepare Data
    |
    v
Save to Database
    |
    v
Import Result
```

Import operations should avoid creating invalid or duplicate records.

## 18. Testing Integration

Testing is integrated into the architecture:

```text
Source Code
    |
    +--> Unit Tests
    +--> Integration Tests
    +--> Security Tests
    +--> System Tests
    +--> Acceptance Tests
    +--> Regression Tests
    +--> Reliability / Recovery Tests
    +--> Frontend Tests
    +--> Playwright E2E
    +--> Accessibility Tests
    +--> Locust Performance Tests
```

This provides multiple levels of verification.

## 19. Deployment Design

The project uses containerization/deployment configuration.

Conceptually:

```text
Docker / Deployment Environment
           |
     +-----+-----+
     |           |
     v           v
 Frontend     Backend
 Container    Container
                  |
                  v
             Database
```

The exact production topology depends on the deployment environment.

## 20. CI/CD Design

The project includes automated quality checks.

```text
Code Change
    |
    v
Git Repository
    |
    v
CI Workflow
    |
    +--> Backend checks/tests
    +--> Frontend tests
    +--> Lint/build
    +--> E2E tests
    |
    v
Quality Gate
    |
    v
Release / Deployment
```

## 21. Maintainability Design

Because this is an individual project, maintainability is especially important.

The design should:

- Keep modules separated.
- Reuse frontend components.
- Keep business logic organized.
- Avoid unnecessary duplication.
- Keep API contracts consistent.
- Maintain regression tests.
- Document important configuration.
- Separate environment-specific settings.
- Use version control.
- Allow future module additions.

## 22. Design Decisions

| Decision | Reason |
|---|---|
| React | Component-based interactive frontend |
| Django | Mature backend framework |
| Django REST Framework | REST API architecture |
| JWT | Token-based API authentication |
| MySQL | Relational data persistence |
| Docker | Reproducible environments |
| Playwright | Browser/E2E testing |
| Locust | Load/performance testing |
| Modular backend apps | Separation of HR domains |
| CI/CD | Automated quality verification |

## 23. Missing Design Artifacts

For a complete academic design package, the following should still be documented:

1. Formal system architecture diagram
2. Detailed ER diagram
3. Complete database schema/data dictionary
4. API endpoint specification
5. Sequence diagrams for major workflows
6. Class/component diagrams where required
7. UI wireframes or screen specifications
8. Detailed security architecture
9. Deployment/network diagram
10. Backup and recovery architecture

These are primarily documentation gaps and do not necessarily require changes to the existing application.

## 24. System Design Conclusion

The HRMS is designed as a layered full-stack web application consisting of a React presentation layer, Django REST application layer, and relational database layer.

The design separates authentication, employee management, attendance, leave, payroll, dashboards, and reporting into logical modules while incorporating security, validation, testing, containerization, and CI/CD.

### System Design Status

**Status: Conceptual design completed.**

The next SDLC stage is **Implementation**, where the design is mapped to the existing source-code structure and implementation decisions are documented.

## Final Design Consistency Review

The design documentation was reviewed against the submitted application structure and SDLC artifacts.

| Design area | Final status |
|---|---|
| Frontend/backend separation | **CONSISTENT** |
| Authentication and authorization | **CONSISTENT** |
| Employee management | **CONSISTENT** |
| Attendance | **CONSISTENT** |
| Leave management | **CONSISTENT** |
| Payroll/payslip | **CONSISTENT** |
| Reporting/export | **CONSISTENT** |
| Database persistence | **CONSISTENT** |
| Docker/deployment configuration | **CONSISTENT** |
| Testing/CI configuration | **CONSISTENT** |
| CSV/PDF export and bulk-import recovery approach | **CONSISTENT** |

### Final Design Closure

The conceptual and implemented design are aligned for the academic submission scope. Detailed diagrams may be maintained as supplementary design evidence; their absence does not change the implemented application behavior.

**Final design/documentation consistency status: COMPLETE**
