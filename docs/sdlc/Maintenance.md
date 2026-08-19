# HR Management System — SDLC Stage 8: Maintenance & Support

## 1. Purpose
This document defines the post-deployment maintenance and support process for the HR Management System (HRMS). It covers corrective, adaptive, perfective, and preventive maintenance after the system has been deployed.

The project is an individual academic project. Therefore, the developer is responsible for triage, maintenance, testing, release, documentation, and recovery activities.

## 2. Scope
Maintenance applies to:
- Authentication and authorization
- Employee management
- Attendance management
- Leave management
- Payroll management 
- Dashboards
- Reports and exports
- Employee profile/self-service
- React frontend
- Django/Django REST backend
- MySQL database
- Docker and CI/CD configuration

## 3. Maintenance Types

### 3.1 Corrective Maintenance
Used to fix defects discovered after release.
Examples:
- Incorrect employee record displayed
- Attendance update failure
- Leave approval error
- Incorrect payroll calculation
- Broken report/export
- API or frontend error

Process:
1. Record the issue.
2. Assign severity.
3. Reproduce the issue.
4. Identify the root cause.
5. Implement the fix in a separate Git branch.
6. Run relevant unit/integration/security/frontend/E2E tests.
7. Review the change.
8. Deploy the fix.
9. Verify the production/staging behavior.
10. Close the issue and record the resolution.

### 3.2 Adaptive Maintenance
Required when the environment changes, such as:
- Django/React/Python/Node dependency updates
- Browser changes
- MySQL version changes
- Hosting-platform changes
- API/library changes
- Operating-system/container changes

### 3.3 Perfective Maintenance
Improves existing capabilities without fixing a defect.
Examples:
- Better report filters
- Improved dashboard visualizations
- Better employee search
- Improved responsive UI
- Additional export options

### 3.4 Preventive Maintenance
Reduces the probability of future failures:
- Dependency vulnerability updates
- Database maintenance
- Log review
- Backup verification
- Test-suite maintenance
- Removal of deprecated code
- CI/CD maintenance

## 4. Maintenance Workflow

```text
Issue / Change Identified
        ↓
Log and classify
        ↓
Impact and root-cause analysis
        ↓
Create Git branch
        ↓
Implement change
        ↓
Run automated tests
        ↓
Code review / verification
        ↓
Deploy
        ↓
Smoke / regression verification
        ↓
Update documentation
        ↓
Close
```

## 5. Maintenance Priority

| Priority | Meaning | Example |
|---|---|---|
| P1 Critical | System unavailable or severe security/data issue | HRMS unavailable |
| P2 High | Major function unavailable | Payroll processing failure |
| P3 Medium | Important non-critical defect | Report filter failure |
| P4 Low | Cosmetic/minor issue | UI alignment issue |

## 6. Release Maintenance Checklist

- [ ] Issue/change recorded
- [ ] Impact assessed
- [ ] Code change committed
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Security tests pass where relevant
- [ ] Frontend tests pass where relevant
- [ ] E2E tests pass where relevant
- [ ] Database migration reviewed where relevant
- [ ] Deployment completed
- [ ] Smoke test completed
- [ ] Documentation updated
- [ ] Change closed

## 7. Maintenance Records
Each significant maintenance activity should record:
- Date
- Issue/change ID
- Description
- Affected module
- Severity
- Root cause
- Fix
- Tests executed
- Release/version
- Result

## 8. Important Boundary
The repository demonstrates extensive testing and CI/CD infrastructure. Production monitoring, formal support operations, backup schedules, and SLA commitments should only be marked as operational after they are actually configured and verified. Otherwise they are treated as planned controls.
