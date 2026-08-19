# HR Management System — SDLC Stage 7: Deployment

## 1. Purpose

This document defines the Deployment stage of the Software Development Life Cycle (SDLC) for the HR Management System (HRMS).

The purpose of deployment is to make the tested application available in a controlled and reproducible environment.

This is an individual academic project, so deployment configuration and deployment activities are managed by the student/developer.

---

## 2. Deployment Objectives

The deployment process aims to:

1. Package the HRMS consistently.
2. Configure frontend, backend and database services.
3. Provide a reproducible application environment.
4. Protect environment-specific secrets and configuration.
5. Run required quality checks before deployment.
6. Provide a predictable startup process.
7. Support recovery from deployment failures.
8. Provide a foundation for future production deployment.

---

## 3. Deployment Architecture

The application is designed as separate application services:

```text
                 User Browser
                     |
                     v
              React Frontend
                     |
                  HTTP/REST
                     |
                     v
              Django Backend
                     |
                     v
                 MySQL DB
```

The project also uses supporting deployment/quality infrastructure:

```text
Git Repository
      |
      v
GitHub Actions
      |
      +--> Tests
      +--> Build
      +--> E2E checks
      |
      v
Docker / Deployment Environment
```

---

## 4. Deployment Components

### 4.1 Frontend

The React application provides the user interface.

Deployment responsibilities include:

- Install frontend dependencies.
- Build the React application.
- Configure the backend/API URL.
- Serve the built frontend using the configured deployment mechanism.

### 4.2 Backend

The Django application provides:

- REST APIs
- Authentication
- Authorization
- Business logic
- Reporting
- Database interaction

Deployment responsibilities include:

- Install Python dependencies.
- Configure Django settings.
- Configure database connectivity.
- Apply database migrations.
- Collect static files where required.
- Start the backend service.

### 4.3 Database

MySQL provides persistent application data.

Deployment responsibilities include:

- Create/configure database.
- Configure credentials securely.
- Apply migrations.
- Verify database connectivity.
- Maintain backup/recovery procedures.

---

## 5. Docker-Based Deployment

The project contains Docker/Docker Compose configuration to support reproducible environments.

Conceptually:

```text
Docker Compose
     |
     +------------------+
     |                  |
     v                  v
 Frontend            Backend
 Container           Container
                         |
                         v
                    Database
```

Docker reduces differences between development and deployment environments.

The exact service names and ports should be taken from the project's Docker Compose configuration.

---

## 6. Environment Configuration

Environment-specific configuration should be kept outside application source code where possible.

Examples include:

- Database name
- Database user
- Database password
- Database host
- Database port
- Django secret key
- Debug setting
- Allowed hosts
- Frontend API URL
- JWT-related configuration

Sensitive credentials must not be committed to the repository.

Environment configuration should distinguish development from deployment/production settings.

---

## 7. Database Deployment

The database deployment process is:

```text
Start Database
      |
      v
Configure Credentials
      |
      v
Connect Backend
      |
      v
Run Migrations
      |
      v
Verify Tables
      |
      v
Application Ready
```

Database migrations must be applied before the application is used against a new database.

---

## 8. Backend Deployment Process

The backend deployment process is:

```text
Obtain Source Code
       |
       v
Install Dependencies
       |
       v
Configure Environment
       |
       v
Run Django Checks
       |
       v
Run Migrations
       |
       v
Collect Static Files
       |
       v
Run Required Tests
       |
       v
Start Backend
```

The backend should not be considered deployment-ready if required checks or tests fail.

---

## 9. Frontend Deployment Process

The frontend deployment process is:

```text
Obtain Source Code
       |
       v
Install Dependencies
       |
       v
Configure API URL
       |
       v
Run Frontend Tests
       |
       v
Run Lint/Build
       |
       v
Generate Production Build
       |
       v
Serve Frontend
```

The frontend must communicate with the correctly configured backend API.

---

## 10. Pre-Deployment Quality Gate

Before deployment, the following should be verified:

- Backend checks pass.
- Backend tests pass.
- Frontend tests pass.
- Linting passes where configured.
- Frontend build succeeds.
- E2E tests pass.
- Required security checks pass.
- Database migrations are valid.
- Environment configuration is present.
- Required secrets are configured securely.

Conceptually:

```text
Code
 |
 v
Automated Tests
 |
 +--> Failure --> Fix --> Re-test
 |
 v
Build
 |
 v
E2E / Quality Checks
 |
 v
Deployment
```

---

## 11. CI/CD Deployment

GitHub Actions provides automated quality verification.

The deployment pipeline is conceptually:

```text
Developer Change
       |
       v
Git Repository
       |
       v
GitHub Actions
       |
       +--> Backend Tests
       +--> Frontend Tests
       +--> Lint
       +--> Build
       +--> Playwright E2E
       |
       v
Quality Gate
       |
       v
Deployment / Release
```

The exact automated deployment steps depend on the configured workflow files and target environment.

---

## 12. Deployment Verification

After deployment, the developer should verify:

### Application availability

- Frontend loads successfully.
- Backend starts successfully.
- Database is reachable.

### Authentication

- Login works.
- JWT authentication works.
- Protected routes are protected.

### Core functionality

- Employee management works.
- Attendance works.
- Leave works.
- Payroll works.
- Dashboard works.
- Reports work.

### Integration

- Frontend communicates with backend.
- Backend communicates with database.
- Report/export functionality works.

### Basic security

- Unauthorized requests are rejected.
- Sensitive configuration is not exposed.
- Production/debug configuration is appropriate.

---

## 13. Deployment Rollback and Recovery

If a deployment fails:

```text
Deployment
    |
    v
Verification
    |
    +--> Pass --> Continue
    |
    +--> Fail
          |
          v
      Investigate
          |
          +--> Fix Configuration
          |
          +--> Roll Back
          |
          v
      Re-deploy
          |
          v
      Verify Again
```

The deployment process should retain a known working version so that a failed release can be reversed.

Database changes require additional care because rolling back application code does not automatically reverse database migrations safely.

---

## 14. Backup and Recovery

A formal operational backup policy should be established before production use.

The policy should define:

- Database backup frequency
- Backup retention period
- Backup storage location
- Recovery procedure
- Recovery Point Objective (RPO)
- Recovery Time Objective (RTO)

For an academic deployment, backups should at minimum be demonstrated or documented for the database and important configuration.

---

## 15. Deployment Security

The deployment environment should:

- Keep secrets outside source code.
- Disable unnecessary debug settings in production.
- Restrict allowed hosts appropriately.
- Use secure database credentials.
- Protect administrative endpoints.
- Use HTTPS in a real production deployment.
- Keep dependencies updated.
- Restrict database access where possible.
- Avoid exposing unnecessary ports/services.

---

## 16. Deployment Environment

The project can be operated in the following environments:

### Development

Used by the individual developer for:

- Coding
- Debugging
- Unit testing
- Integration testing

### Test/CI

Used for:

- Automated tests
- Build verification
- E2E testing
- Quality checks

### Deployment/Production

Used for:

- Running the application for actual users
- Maintaining persistent data
- Monitoring and recovery

The exact production hosting provider is environment-dependent and should be documented when selected.

---

## 17. Deployment Checklist

Before a deployment:

- [ ] Source code is committed.
- [ ] Required tests pass.
- [ ] Frontend build succeeds.
- [ ] Backend checks pass.
- [ ] Database migrations are verified.
- [ ] Environment variables are configured.
- [ ] Secrets are protected.
- [ ] Docker/services start successfully.
- [ ] E2E tests pass where required.
- [ ] Backup/recovery arrangements are available.
- [ ] Deployment version is identifiable.

After deployment:

- [ ] Frontend loads.
- [ ] Backend API responds.
- [ ] Database connection works.
- [ ] Login works.
- [ ] Employee workflows work.
- [ ] Attendance workflows work.
- [ ] Leave workflows work.
- [ ] Payroll workflows work.
- [ ] Reports work.
- [ ] No critical errors are present.

---

## 18. Deployment Gaps

The existing project has strong deployment foundations through Docker and CI/CD, but the following should be formally documented for a complete production deployment process:

1. Exact production hosting environment.
2. Production environment variable specification.
3. HTTPS/TLS configuration.
4. Domain/DNS configuration.
5. Database backup schedule.
6. Monitoring and alerting.
7. Log retention.
8. Rollback procedure for database migrations.
9. Formal RPO/RTO targets.
10. Production security checklist.

These are mainly operational deployment/documentation gaps.

---

## 19. Deployment Conclusion

The HRMS has the core configuration required for reproducible deployment through Docker and automated quality verification through CI/CD.

The deployment process should ensure that the application is tested, configured, migrated, started and verified before being made available to users.

### Deployment Status

**Status: Deployment infrastructure implemented; production operations documentation requires further definition.**

The next SDLC stage is **Maintenance**.
