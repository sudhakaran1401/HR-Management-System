# Exploratory Testing

## Objective

Use session-based exploration to discover unexpected behavior in the HRMS by testing normal and unusual user interactions across major application modules.

## Areas Tested

- Authentication and Authorization
- Employee Management
- Attendance
- Leave
- Payroll
- Reports

## Exploratory Testing Results

### Authentication and Authorization

One suspicious behavior was observed during authentication testing.

#### Finding EX-001 — Username Case Sensitivity

| Field | Details |
|---|---|
| Finding ID | EX-001 |
| Area | Authentication |
| Issue | Username with different letter casing is accepted |
| Steps | 1. Enter valid username `ajay.patel`. 2. Enter valid password `Ajay@123`. 3. Login successfully. 4. Change the username to `Ajay patel` while keeping the same password. 5. Attempt to log in. |
| Expected Result | If usernames are case-sensitive, `Ajay.patel` should be rejected because it differs from `ajay.patel`. |
| Actual Result | `Ajay.patel` is accepted and login is successful with the same password. |
| Severity | Low / Medium — requires verification against the intended username policy |
| Status | Observation — requires verification |

> This behavior is not classified as a confirmed defect until the application's intended username policy is verified. Some systems intentionally treat usernames as case-insensitive.

### Employee Management

No unexpected behavior was observed during exploratory testing.

### Attendance

No unexpected behavior was observed during exploratory testing.

### Leave

No unexpected behavior was observed during exploratory testing.

### Payroll

No unexpected behavior was observed during exploratory testing.

### Reports

No unexpected behavior was observed during exploratory testing.

## Summary

| Area | Result |
|---|---|
| Authentication and Authorization | 1 observation requiring verification |
| Employee Management | No unexpected behavior observed |
| Attendance | No unexpected behavior observed |
| Leave | No unexpected behavior observed |
| Payroll | No unexpected behavior observed |
| Reports | No unexpected behavior observed |

## Conclusion

Exploratory testing was performed across authentication and authorization, employee management, attendance, leave, payroll, and reports. No unexpected behavior was observed in Employee Management, Attendance, Leave, Payroll, or Reports.

One observation was identified in authentication: usernames with different letter casing were accepted with the same password. This behavior should be verified against the application's intended username policy before being classified as a defect.
