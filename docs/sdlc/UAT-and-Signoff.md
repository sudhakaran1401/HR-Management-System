# HR Management System — User Acceptance Testing (UAT) & Sign-off

## 1. Purpose

UAT verifies that the HRMS supports the expected real-world HR workflows from the perspective of its intended users.

The project is an individual academic project. Therefore, UAT is performed as a formal simulated stakeholder acceptance exercise. The UAT scenarios below have been executed against the HRMS and all scenarios passed.

## 2. UAT Roles

- **HR/Admin:** validates administrative HR workflows.
- **Employee:** validates employee self-service.
- **Developer:** prepares the environment, fixes defects and records evidence.

## 3. UAT Execution Results

| ID | Role | Scenario | Expected Result | Status |
|---|---|---|---|---|
| UAT-01 | HR/Admin | Login with valid credentials | HR dashboard opens | **PASS** |
| UAT-02 | Employee | Login with valid credentials | Employee dashboard opens | **PASS** |
| UAT-03 | HR/Admin | Create employee | Employee record is created and listed | **PASS** |
| UAT-04 | HR/Admin | Edit employee | Updated information is displayed | **PASS** |
| UAT-05 | HR/Admin | Delete employee | Employee is removed according to workflow | **PASS** |
| UAT-06 | Employee | View profile | Own profile is displayed | **PASS** |
| UAT-07 | HR/Admin | Mark/update attendance | Attendance is stored correctly | **PASS** |
| UAT-08 | Employee | View attendance history/calendar | Own attendance is displayed | **PASS** |
| UAT-09 | Employee | Apply for leave | Request becomes pending | **PASS** |
| UAT-10 | HR/Admin | Approve leave | Request becomes approved | **PASS** |
| UAT-11 | HR/Admin | Reject leave | Request becomes rejected | **PASS** |
| UAT-12 | Employee | View leave balance | Current balance is displayed | **PASS** |
| UAT-13 | HR/Admin | Create/update payroll | Payroll record is calculated/stored | **PASS** |
| UAT-14 | Employee | View/download payslip | Own payslip is available | **PASS** |
| UAT-15 | HR/Admin | Generate report | Correct filtered report is produced | **PASS** |
| UAT-16 | HR/Admin | Export report | Supported file/download is generated | **PASS** |
| UAT-17 | Unauthorized user | Access restricted HR function | Access is denied | **PASS** |
| UAT-18 | User | Logout | Session/access is terminated | **PASS** |
| UAT-19 | User | Use mobile/responsive layout | Core functions remain usable | **PASS** |
| UAT-20 | User | Switch theme | UI changes correctly without breaking function | **PASS** |

### UAT-19 Compatibility Evidence

The responsive/mobile acceptance scenario is additionally supported by the project's compatibility testing. The compatibility testing verifies the HRMS across the supported browser/device or viewport combinations defined by the project.

## 4. UAT Acceptance Criteria

The release is accepted when:

- All critical scenarios pass.
- No open P1 defects remain.
- Security/authorization checks pass.
- Payroll and leave workflows produce expected results.
- Reports and exports work for supported scenarios.
- Any accepted limitations are documented.

**UAT result:** All 20 defined UAT scenarios passed.

## 5. Defect Handling

Any failed UAT scenario is recorded as a defect with:

- UAT ID
- Description
- Severity
- Steps to reproduce
- Expected result
- Actual result
- Fix
- Retest result

No UAT scenario remained failed after the completed UAT execution.

## 6. Evidence

Recommended evidence to retain with the project submission:

- Screenshots or screen recordings for representative UAT workflows.
- Compatibility-test results supporting UAT-19.
- Test results for payroll, leave and authorization workflows.
- Export/report evidence supporting UAT-16.

## 7. Acceptance Record

**Release:** ____________________

**UAT execution date:** ____________________

**Overall result:** **PASS**

**Known limitations:**  
No known UAT-blocking limitations identified during the completed UAT scenarios.

**Prepared by:** ____________________

**Reviewed/accepted by:** ____________________

**Date:** ____________________

**Signature (if required):** ____________________

## 8. Final UAT Status

**Status: PASS**

The HRMS completed the defined UAT scenarios successfully. The UAT confirms business-level acceptance of the implemented HR, employee self-service, attendance, leave, payroll, reporting, authorization, responsive-layout and theme workflows.

Automated and other technical tests in the repository provide technical verification, while this document records the formal business/user acceptance layer.
