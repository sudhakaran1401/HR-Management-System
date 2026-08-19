# HR Management System — Incident & Support Process

## 1. Purpose
This document defines how operational incidents, user-reported problems, security issues and support requests are handled after deployment.

## 2. Incident vs Service Request

**Incident:** Something that worked or should work has failed or degraded.

Examples:
- Login failure
- HR dashboard unavailable
- Payroll calculation failure
- Database unavailable
- Report download failure

**Service Request:** A normal request that does not represent a failure.

Examples:
- Request for a new report
- Request for a new field
- Request for a UI improvement

Service requests should follow the Change Management process when implementation is required.

## 3. Severity

| Severity | Definition | Example |
|---|---|---|
| P1 Critical | System unavailable, severe data/security impact | Complete HRMS outage |
| P2 High | Major business function unavailable | Payroll unavailable |
| P3 Medium | Important but workaround exists | Attendance report issue |
| P4 Low | Minor defect/request | UI issue |

## 4. Incident Workflow

```text
Incident Detected
      ↓
Record incident
      ↓
Classify severity
      ↓
Contain / protect data
      ↓
Investigate
      ↓
Root-cause analysis
      ↓
Fix or rollback
      ↓
Test
      ↓
Deploy
      ↓
Verify
      ↓
Close
      ↓
Post-incident review
```

## 5. Incident Record

| Field | Value |
|---|---|
| Incident ID | |
| Date/time detected | |
| Reporter | |
| Affected module | |
| Severity | |
| Description | |
| Business impact | |
| Steps to reproduce | |
| Root cause | |
| Immediate action | |
| Permanent fix | |
| Release/commit | |
| Tests performed | |
| Recovery time | |
| Closure date | |

## 6. Security Incidents
Security incidents require priority handling. Examples:
- Unauthorized access
- Credential/token exposure
- Privilege escalation
- Sensitive report exposure
- Suspicious authentication behavior

Immediate actions may include:
- Revoke/rotate affected credentials or tokens.
- Restrict affected access.
- Preserve relevant logs.
- Identify affected records.
- Patch the vulnerability.
- Run security regression tests.
- Document the incident.

## 7. User Support
Support requests should capture:
- User/role
- Module
- Description
- Screenshot/log evidence where appropriate
- Expected behavior
- Actual behavior
- Priority

## 8. Root-Cause Analysis
For P1/P2 incidents, document:
- What happened?
- Why did it happen?
- Why was it not detected earlier?
- What fixed it?
- What prevents recurrence?
- Which tests/documentation should be updated?

## 9. Support Ownership
For this individual academic project, the developer is the support owner. In a real deployment, support ownership should be assigned to an HR/application support team with defined escalation contacts.

## 10. Closure Criteria
An incident can be closed when:
- Root cause is understood or documented as an accepted limitation.
- Fix/recovery is completed.
- Relevant tests pass.
- User/business impact is resolved.
- Documentation is updated where needed.
- Follow-up preventive actions are recorded.
