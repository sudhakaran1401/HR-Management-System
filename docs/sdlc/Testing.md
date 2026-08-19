# HR Management System — SDLC Stage 6: Testing

## 1. Purpose

This document defines the Testing stage of the Software Development Life Cycle (SDLC) for the HR Management System (HRMS).

The purpose of testing is to verify that the implemented system:

- Meets its functional requirements.
- Enforces security and authorization rules.
- Handles invalid inputs correctly.
- Integrates frontend, backend and database components correctly.
- Performs reliably under expected conditions.
- Supports browser-based workflows.
- Maintains accessibility.
- Continues to work after changes.

This is an individual academic project, so all test planning, execution, defect fixing and verification are performed by the student/developer.

---

## 2. Testing Objectives

The testing process aims to:

1. Verify core HR functionality.
2. Detect defects before deployment.
3. Verify authentication and authorization.
4. Verify business rules for attendance, leave and payroll.
5. Verify frontend/backend integration.
6. Verify error and recovery behavior.
7. Verify regression after code changes.
8. Verify end-to-end user workflows.
9. Verify accessibility.
10. Evaluate application performance under load.
11. Provide evidence that the implemented requirements are satisfied.

---

## 3. Testing Strategy

The HRMS uses multiple levels of testing:

```text
Unit Testing
     ↓
Integration Testing
     ↓
Security Testing
     ↓
System Testing
     ↓
Acceptance Testing
     ↓
Regression Testing
     ↓
Reliability / Recovery Testing
     ↓
Frontend Testing
     ↓
End-to-End Testing
     ↓
Accessibility Testing
     ↓
Performance Testing
```

Testing is not limited to a final testing phase. Tests are also used during development and CI/CD.

---

## 4. Unit Testing

Unit tests verify small pieces of application functionality independently.

Examples include:

- Employee validation
- Attendance rules
- Leave calculations/validation
- Payroll calculations
- Utility functions
- API/service logic

### Purpose

Unit testing helps identify defects at the smallest practical level before functionality is integrated with other components.

### Status

**Implemented**

The backend contains a substantial unit/application test suite.

---

## 5. Integration Testing

Integration tests verify that multiple application components work together.

Examples include:

- API + database
- Authentication + protected API
- Employee + attendance
- Employee + leave
- Employee + payroll
- Payroll + related business data
- Frontend service + backend API

### Purpose

Integration testing identifies defects that may not be visible when individual components are tested separately.

### Status

**Implemented**

The existing project contains integration-focused tests.

---

## 6. Security Testing

Security testing verifies that sensitive HR functionality is protected.

Areas include:

- Authentication
- Authorization
- Protected endpoints
- Role-based access
- Unauthorized access attempts
- Employee data isolation
- Administrative functionality

Important scenarios include:

```text
Unauthenticated User
        |
        v
Protected API
        |
        v
Access Denied
```

and:

```text
Employee User
     |
     v
HR-Only Operation
     |
     v
Access Denied
```

### Status

**Implemented**

The project contains security-focused tests.

---

## 7. System Testing

System testing verifies the complete application as an integrated system.

Major system areas include:

- Login
- Employee management
- Attendance
- Leave
- Payroll
- Dashboard
- Reports
- Role-based access

System testing verifies that the complete system behaves according to its requirements.

### Status

**Implemented**

---

## 8. Acceptance Testing

Acceptance testing verifies that major user-facing workflows satisfy expected business behavior.

Examples:

### Employee workflow

```text
Login
  ↓
View Profile
  ↓
View Attendance
  ↓
Apply Leave
  ↓
View Payroll
```

### HR workflow

```text
Login
  ↓
Manage Employee
  ↓
Manage Attendance
  ↓
Review Leave
  ↓
Manage Payroll
  ↓
Generate Reports
```

### Status

**Implemented**

Acceptance/system-level tests are present for major application behavior.

---

## 9. Regression Testing

Regression testing verifies that previously working functionality remains functional after changes.

Regression areas include:

- Authentication
- Employee operations
- Attendance
- Leave
- Payroll
- Dashboard
- APIs
- Frontend workflows

Regression testing is especially important because changes in shared models, APIs or authentication can affect multiple modules.

### Status

**Implemented**

---

## 10. Reliability Testing

Reliability testing checks whether the system continues to operate correctly during repeated or expected operations.

Examples include:

- Repeated API operations
- Repeated valid transactions
- Repeated access to protected resources
- Handling expected application failures
- Maintaining data consistency

### Status

**Implemented**

---

## 11. Recovery Testing

Recovery testing verifies how the system behaves after errors or failed operations.

Examples include:

- Invalid requests
- Failed operations
- Database/application errors
- Recovery after an unsuccessful transaction
- Ensuring invalid operations do not corrupt data

### Status

**Implemented**

---

## 12. Frontend Testing

Frontend tests verify React application behavior.

Testing areas include:

- Login
- Protected routes
- Employee pages
- Attendance
- Leave
- Payroll
- Dashboard
- API services
- Download/report services
- Hooks
- Utility functions
- Reusable components

Frontend testing verifies that UI components and client-side logic behave correctly.

### Status

**Implemented**

---

## 13. End-to-End Testing

Playwright is used for browser-based end-to-end testing.

E2E testing verifies complete user workflows through the actual application interface.

Examples include:

- Login
- Navigation
- Employee workflows
- Attendance workflows
- Leave workflows
- Payroll workflows
- Protected-route behavior

Conceptual flow:

```text
Browser
   ↓
React UI
   ↓
REST API
   ↓
Django
   ↓
Database
   ↓
Response
   ↓
Browser
```

### Status

**Implemented**

The project contains Playwright E2E tests.

---

## 14. Accessibility Testing

Accessibility testing is performed using browser-based testing with Axe/Playwright.

The purpose is to identify accessibility problems in application pages and interfaces.

Examples of accessibility concerns include:

- Missing accessible labels
- Incorrect semantic structure
- Keyboard-accessibility problems
- Color/contrast-related issues detected by automated checks
- Other detectable WCAG-related violations

### Status

**Implemented**

Automated accessibility checks are included in the project.

---

## 15. Performance and Load Testing

Locust is used to evaluate system behavior under increasing user load.

The project includes a stress-testing approach involving increasing concurrent users.

Performance testing focuses on areas such as:

- Authentication
- API requests
- Employee operations
- Attendance
- Leave
- Payroll
- Dashboard/report operations

Conceptual load progression:

```text
Normal Load
    ↓
10 Users
    ↓
50 Users
    ↓
100 Users
    ↓
250 Users
    ↓
500 Users
```

The purpose is to identify performance degradation and capacity limitations.

### Status

**Implemented**

---

## 16. Test Environment

Testing uses the project's configured application environment.

The environment includes:

- Django backend
- React frontend
- Database
- Browser environment
- Playwright
- Axe
- Locust
- CI environment

Docker can be used to provide a reproducible environment where applicable.

---

## 17. Test Data

Testing should use controlled development/test data.

Examples include:

- Test users
- Test employees
- Attendance records
- Leave records
- Payroll records
- Invalid input data
- Duplicate records
- Boundary values

Real sensitive employee information should not be used as test data without appropriate authorization and protection.

---

## 18. Important Test Scenarios

### Authentication

- Valid login
- Invalid login
- Missing credentials
- Protected endpoint without authentication
- Invalid/expired token

### Employee Management

- Create valid employee
- Update employee
- Retrieve employee
- Invalid employee input
- Duplicate employee data
- Unauthorized employee access

### Attendance

- Create valid attendance
- Duplicate attendance
- Invalid employee
- Invalid date
- View attendance
- Attendance filtering/reporting

### Leave

- Submit valid leave
- Invalid date range
- Overlapping leave
- Leave approval
- Leave rejection
- Leave balance
- Unauthorized leave operations

### Payroll

- Create payroll
- Calculate gross salary
- Calculate deductions
- Calculate net salary
- Duplicate payroll period
- Invalid payroll data
- Employee payroll access

### Security

- Unauthenticated access
- Unauthorized role access
- Employee accessing another employee's information
- HR/Admin protected operations

### Frontend

- Login interface
- Navigation
- Protected routes
- Forms
- Tables
- Dashboard
- Error/loading states

---

## 19. Test Execution Process

The individual developer follows this general process:

```text
Requirement
    ↓
Identify Test Scenario
    ↓
Create/Update Test
    ↓
Run Test
    |
    +--> Pass --> Record Result
    |
    +--> Fail
           ↓
        Investigate
           ↓
        Fix Defect
           ↓
        Re-run Test
           ↓
        Regression Test
```

---

## 20. Defect Management

When a test fails, the developer should record:

- Defect description
- Affected module
- Steps to reproduce
- Expected result
- Actual result
- Severity
- Root cause where known
- Fix
- Verification result

Defects should be prioritized according to their impact.

Example severity levels:

| Severity | Meaning |
|---|---|
| Critical | System/security failure preventing safe operation |
| High | Major business functionality is unusable |
| Medium | Important functionality is affected but workaround exists |
| Low | Minor UI/documentation/non-critical issue |

---

## 21. CI/CD Testing

Automated testing is integrated into the project's CI workflow.

Conceptually:

```text
Code Change
    ↓
CI Pipeline
    ↓
Backend Checks
    ↓
Backend Tests
    ↓
Frontend Tests
    ↓
Lint / Build
    ↓
Playwright E2E
    ↓
Quality Gate
```

This provides automated verification whenever code changes are introduced.

---

## 22. Testing Traceability

| Requirement Area | Main Testing |
|---|---|
| Authentication | Unit, integration, security, E2E |
| Authorization | Security, integration, E2E |
| Employee management | Unit, integration, system, E2E |
| Attendance | Unit, integration, system, E2E |
| Leave | Unit, integration, regression, E2E |
| Payroll | Unit, integration, regression, E2E |
| Dashboard | Frontend, system, E2E |
| Reports | Integration, frontend/E2E |
| Data validation | Unit, integration |
| Reliability | Reliability tests |
| Recovery | Recovery tests |
| Accessibility | Axe/Playwright |
| Performance | Locust |
| Overall application | System/acceptance/E2E |

---

## 23. Testing Strengths of the Existing Project

The HRMS has strong testing coverage compared with a project that only contains basic unit tests.

Major strengths include:

- Multiple backend test levels
- Security testing
- Regression testing
- Reliability and recovery testing
- Frontend testing
- Browser-based E2E testing
- Accessibility testing
- Performance/load testing
- CI-based automated testing

This makes testing one of the strongest SDLC areas of the current HRMS.

---

## 24. Testing Gaps

Although testing is extensive, the following should be formally improved or maintained:

1. Define explicit pass/fail thresholds for performance tests.
2. Maintain a complete requirement-to-test traceability matrix.
3. Document test execution results and dates.
4. Record defects and their resolutions.
5. Define formal test entry and exit criteria.
6. Define supported browser versions.
7. Add additional security checks as production requirements evolve.
8. Maintain regression tests whenever functionality changes.

These are primarily documentation and continuous-improvement requirements rather than evidence that testing is absent.

---

## 25. Test Entry Criteria

Testing for a feature should begin when:

- The relevant implementation is available.
- Required test data is available.
- The environment is functional.
- The expected behavior is defined.
- Relevant test cases are prepared.

---

## 26. Test Exit Criteria

A release/test cycle should be considered complete when:

- Planned tests have been executed.
- Critical/high-severity defects are resolved or formally accepted.
- Required regression tests pass.
- E2E tests pass.
- Security checks pass for affected functionality.
- Required performance checks meet defined targets.
- Test results are documented.

---

## 27. Testing Conclusion

The HRMS has a comprehensive multi-level testing approach covering backend, frontend, security, integration, system, acceptance, regression, reliability, recovery, E2E, accessibility and performance testing.

The main remaining work is to formalize test documentation such as execution records, defect records, explicit thresholds, entry/exit criteria and complete requirements-to-test traceability.

### Testing Status

**Status: Implemented and substantially complete**

The next SDLC stage is **Deployment**.


---

## Final Regression Verification

The final regression gate and evidence requirements are recorded in:

`docs/sdlc/Final-Regression-Verification.md`

**Current status: READY FOR FINAL REGRESSION EXECUTION**
