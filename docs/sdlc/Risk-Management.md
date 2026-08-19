# HR Management System — Risk Management

## 1. Purpose
This document identifies project, technical, security, operational, and data risks and defines mitigation and contingency actions.

## 2. Risk Scoring

Probability and impact are rated Low (1), Medium (2), or High (3).

Risk Score = Probability × Impact.

| Score | Level |
|---|---|
| 1–2 | Low |
| 3–4 | Medium |
| 6–9 | High |

## 3. Risk Register

| ID | Risk | Probability | Impact | Score | Mitigation | Contingency |
|---|---|---:|---:|---:|---|---|
| R-01 | Unauthorized access to HR/payroll data | M | H | 6 | JWT, role checks, protected routes/APIs, security tests | Disable affected access, rotate credentials/tokens, investigate |
| R-02 | Employee/payroll data loss | L | H | 3 | Scheduled database backups and restore verification | Restore latest verified backup |
| R-03 | Database outage/corruption | M | H | 6 | Database monitoring, backups, integrity checks | Restore/recover database |
| R-04 | Incorrect payroll calculation | M | H | 6 | Automated payroll tests, validation and review | Correct affected records and rerun payroll |
| R-05 | Leave balance/overlap errors | M | M | 4 | Model validation and leave tests | Correct request/balance and add regression test |
| R-06 | Deployment failure | M | H | 6 | CI/CD, Docker, automated tests | Roll back to last known-good release |
| R-07 | Dependency vulnerability | M | H | 6 | Dependency review and security updates | Patch/upgrade affected dependency |
| R-08 | Breaking framework/browser update | M | M | 4 | Version control and compatibility testing | Pin/rollback dependency and release fix |
| R-09 | CI/CD pipeline failure | M | M | 4 | Maintain separate CI checks and inspect failures | Manual verified deployment if appropriate |
| R-10 | Incorrect imported Excel data | M | M | 4 | Input validation and import testing | Reject/repair source file and re-import |
| R-11 | Sensitive data exposed through reports/downloads | L | H | 3 | Authorization checks and security tests | Disable affected export and rotate access |
| R-12 | Service outage | L | H | 3 | Health checks, logs and deployment verification | Recovery/rollback procedure |
| R-13 | Loss of project source/history | L | H | 3 | Git repository and release tags | Restore repository/version |
| R-14 | Incomplete requirements coverage | M | M | 4 | RTM and acceptance review | Add missing requirement/test before release |
| R-15 | Single-developer dependency | H | M | 6 | Documentation, Git history and repeatable setup | Use documented recovery/deployment procedures |

## 4. Security Risk Controls
Sensitive HR data includes employee identity/profile information and payroll information. Controls include:
- Authentication
- Authorization
- Protected routes
- Protected APIs
- Input validation
- Security testing
- Secure environment configuration
- Controlled report/export access

## 5. Risk Review
Risks should be reviewed:
- Before major releases
- After critical incidents
- After major dependency changes
- After database/schema changes
- When new HR functionality is introduced

## 6. Risk Ownership
For this individual academic project, the developer is the primary risk owner. In a real organization, risks should be assigned to named business/technical owners.
