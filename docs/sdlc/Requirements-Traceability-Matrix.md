# HR Management System — Requirements Traceability Matrix (RTM)

## 1. Purpose
The RTM connects business requirements to implemented modules and verification evidence. It demonstrates that requirements are implemented and tested rather than documented in isolation.

## 2. Traceability Structure

```text
Requirement → Module → Implementation → Test Evidence → Acceptance
```

## 3. Functional Requirements

| ID | Requirement | Module / Area | Implementation Evidence | Verification |
|---|---|---|---|---|
| FR-01 | Secure user login | Accounts / Frontend Login | JWT authentication, login page, protected routes | Authentication + login tests |
| FR-02 | Role-based access | Accounts / Employees / Leave / Attendance / Payroll | Role/group checks, protected routes and APIs | Security tests |
| FR-03 | Employee CRUD | Employees | Employee model, forms, list/detail/create/update/delete views | Employee unit/integration/frontend tests |
| FR-04 | Employee self-profile | Employees / Profile | Employee profile association and profile views | Profile/frontend tests |
| FR-05 | Employee Excel import | Employees / Import | Excel import command and sample workbook | Import/validation tests where applicable |
| FR-06 | Attendance recording | Attendance | Attendance model and attendance views/forms | Attendance tests |
| FR-07 | Attendance calendar | Attendance / Frontend | Calendar page and events endpoint | Calendar/frontend tests |
| FR-08 | Attendance reports | Attendance / Reports | Report/filter/export functions | Report tests |
| FR-09 | Attendance Excel import | Attendance / Import | Import command and sample workbook | Import tests where applicable |
| FR-10 | Leave application | Leave | LeaveRequest model and employee leave workflow | Leave tests |
| FR-11 | Leave approval/rejection | Leave / HR | Status workflow and HR controls | Leave integration/security tests |
| FR-12 | Leave balance | Leave | LeaveBalance model and employee dashboard | Leave-balance tests |
| FR-13 | Leave overlap validation | Leave | Model validation for overlapping requests | Leave validation tests |
| FR-14 | Leave reports/export | Leave / Reports | Report and export functions | Report tests |
| FR-15 | Payroll processing | Payroll | SalaryHistory model and salary calculation logic | Payroll tests |
| FR-16 | Payroll locking/finalization | Payroll | is_locked/is_finalized fields and workflow | Payroll/security tests |
| FR-17 | Payslip generation/view/download | Payroll / Frontend | Payslip view and PDF/report utilities | Payroll/download tests |
| FR-18 | Payroll Excel import | Payroll / Import | Import command and sample workbook | Import tests where applicable |
| FR-19 | HR dashboard | Dashboard | HR dashboard view and React dashboard components | Dashboard tests |
| FR-20 | Employee dashboard | Dashboard | Employee dashboard view/components | Dashboard tests |
| FR-21 | Reports and charts | Reports | Employee, attendance, leave and payroll reports | Report/frontend tests |
| FR-22 | Search/filter/pagination | Frontend / Backend | Search bars, filters, table pagination, django-filter | Component/API tests |
| FR-23 | Secure logout | Accounts | Logout flow and token/session handling | Authentication tests |
| FR-24 | Responsive/dark UI | Frontend | Bootstrap/responsive layouts/theme toggle | Frontend/usability/accessibility testing |
| FR-25 | Error/loading feedback | Frontend | Alert, loader, error-handling components | Component/frontend tests |

## 4. Non-Functional Requirements

| ID | Requirement | Evidence |
|---|---|---|
| NFR-01 | Security | JWT, protected APIs/routes, security tests |
| NFR-02 | Reliability | Reliability/recovery test suites |
| NFR-03 | Maintainability | Modular Django apps, React components/hooks/services |
| NFR-04 | Usability | Usability testing documentation |
| NFR-05 | Accessibility | Axe/Playwright accessibility testing |
| NFR-06 | Compatibility | Browser compatibility testing |
| NFR-07 | Performance | Load/performance testing infrastructure |
| NFR-08 | Deployability | Docker, Docker Compose, CI/CD workflows |
| NFR-09 | Data integrity | Model validation, unique constraints and database relationships |
| NFR-10 | Regression resistance | Automated regression/frontend/E2E tests |

## 5. Traceability Review Rules
- Every requirement must have an implementation location.
- Every critical requirement must have a verification test.
- Failed requirements must be tracked as defects or change requests.
- New requirements receive a new ID.
- Changed requirements must be updated in the RTM and related tests.

## 6. Status Convention

| Status | Meaning |
|---|---|
| Implemented | Functionality exists in the repository |
| Verified | Corresponding test evidence exists |
| Partially Verified | Functionality exists but complete test evidence is not yet mapped |
| Planned | Requirement is documented but not implemented |
| Deferred | Intentionally postponed |

This RTM should be updated whenever a requirement, implementation, or test changes.

## Final Verification

The RTM was reviewed against the submitted HRMS requirements, implementation modules, and available verification/UAT evidence.

| Final check | Status |
|---|---|
| Requirements are identified in the RTM | **COMPLETE** |
| Requirements have implementation/module mapping | **COMPLETE** |
| Requirements have verification/test coverage where applicable | **COMPLETE** |
| UAT coverage is recorded separately | **COMPLETE** |
| BDR/recovery capability is recorded separately | **COMPLETE** |
| Unmapped critical requirement identified during final review | **NONE IDENTIFIED** |

**Final RTM status: COMPLETE**

This RTM is the baseline for the submitted academic release. Future requirement changes must update the RTM and the corresponding implementation and verification evidence.
