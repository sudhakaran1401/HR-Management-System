# HR Management System — Change & Version Management

## 1. Purpose
This document defines how source-code, database, configuration, documentation, and functional changes are controlled.

The repository already uses Git and GitHub Actions. This document formalizes the process around those tools.

## 2. Change Categories

| Category | Example |
|---|---|
| Functional | Add employee search |
| Defect | Fix payroll calculation |
| Security | Fix authorization issue |
| Database | Add/modify model field |
| UI/UX | Improve dashboard |
| Dependency | Upgrade Django/React package |
| Infrastructure | Modify Docker/CI/CD |
| Documentation | Update SDLC/RTM |

## 3. Change Workflow

```text
Change Request / Defect
        ↓
Record change
        ↓
Impact analysis
        ↓
Approve / prioritize
        ↓
Create Git branch
        ↓
Implement
        ↓
Run tests
        ↓
Review
        ↓
Merge
        ↓
Create release/version
        ↓
Deploy
        ↓
Verify
        ↓
Update documentation
```

## 4. Git Practices
Recommended branch pattern:
- `main` — stable/releasable code
- `feature/<name>` — new functionality
- `fix/<name>` — defect fixes
- `security/<name>` — security fixes
- `docs/<name>` — documentation-only changes

Example:
`feature/payroll-report-filter`

## 5. Commit Guidance
Commits should describe one logical change.

Examples:
- `feat: add employee report filter`
- `fix: prevent overlapping leave requests`
- `test: add payroll calculation coverage`
- `docs: add maintenance process`

## 6. Pull Request / Review
Before merging a significant change:
- Explain the change.
- Identify affected modules.
- Identify database changes.
- Identify security implications.
- Identify tests performed.
- Confirm CI checks pass.

For an individual project, the developer may perform self-review using the same checklist.

## 7. Versioning
Use release tags for stable milestones, for example:
- `v1.0.0` — initial stable release
- `v1.1.0` — backward-compatible feature release
- `v1.1.1` — bug/security fix

## 8. Database Changes
Any schema change must:
1. Update the Django model.
2. Create/check migrations.
3. Test migration locally.
4. Verify affected functionality.
5. Back up production data before a risky migration.
6. Document rollback/recovery considerations.

## 9. Change Record

| Field | Description |
|---|---|
| Change ID | Unique identifier |
| Date | Date requested |
| Request | Description |
| Reason | Why it is needed |
| Impact | Modules/data affected |
| Risk | Low/Medium/High |
| Implementation | Git branch/commit |
| Tests | Tests executed |
| Release | Version/tag |
| Result | Completed/rejected/deferred |

## 10. Rollback
If a release introduces a critical regression:
- Stop further rollout.
- Identify the last known-good version.
- Roll back application code/container.
- Restore database only when necessary and after impact assessment.
- Verify core login, employee, attendance, leave and payroll workflows.
- Record the incident and root cause.
