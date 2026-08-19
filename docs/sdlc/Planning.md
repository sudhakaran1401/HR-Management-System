# HR Management System — SDLC Stage 1: Planning

## 1. Project Overview

The HR Management System (HRMS) is an individual academic software project developed as a web-based application to centralize and simplify core human-resource operations.

The system provides functionality for employee management, attendance, leave, payroll, authentication, authorization, dashboards, reporting, testing, and deployment.

This document formally defines the Planning stage of the Software Development Life Cycle (SDLC) for the individual project.

---

## 2. Project Type

**Project Type:** Individual Academic Project

The entire project is planned, designed, developed, tested, documented, and maintained by a single developer/student.

The developer is responsible for all major SDLC activities:

- Project planning
- Requirements analysis
- System analysis
- System design
- Database design
- Frontend development
- Backend development
- Integration
- Testing
- Deployment
- Documentation
- Maintenance

External tools and frameworks may be used, but project decisions and implementation are managed individually.

---

## 3. Problem Statement

Traditional or fragmented HR processes can result in:

- Duplicate or inconsistent employee records
- Manual attendance tracking
- Errors in leave calculations and approvals
- Payroll calculation errors
- Difficulty retrieving employee information
- Unauthorized access to sensitive HR information
- Time-consuming report generation

The HRMS is planned to provide a centralized and controlled system for managing these activities digitally.

---

## 4. Project Objectives

### Primary Objective

To develop a secure and centralized web-based HR management system that supports the organization's core employee-management processes.

### Specific Objectives

1. Manage employee information digitally.
2. Provide secure user authentication.
3. Implement role-based authorization.
4. Manage employee attendance.
5. Manage leave applications and approvals.
6. Support payroll processing and calculations.
7. Provide dashboards and reports.
8. Reduce manual HR workload.
9. Improve data accuracy and consistency.
10. Protect sensitive employee and payroll information.
11. Implement automated testing to verify system quality.
12. Provide a maintainable and deployable application.
13. Apply the SDLC systematically throughout the individual project.

---

## 5. Stakeholders

Although this is an individual development project, the finished system has several stakeholders/users.

| Stakeholder | Interest / Responsibility |
|---|---|
| Student/Developer | Responsible for planning, analysis, design, development, testing, deployment, documentation and maintenance |
| System Administrator | Manages users, system configuration and access permissions |
| HR Personnel | Manages employees, attendance, leave, payroll and reports |
| Employees | View personal information, attendance, leave and payroll details |
| Management | Reviews HR information and reports |
| Project Evaluator/Supervisor | Reviews the project, implementation and SDLC documentation |

---

## 6. Project Scope

### 6.1 In-Scope

The project includes:

- User authentication
- User authorization and role management
- Employee management
- Employee profiles
- Attendance management
- Leave management
- Leave approval/rejection
- Payroll management
- Payroll calculations
- Dashboard functionality
- Reports
- Backend REST APIs
- React-based frontend
- Database management
- Automated backend testing
- Frontend testing
- End-to-end testing
- Accessibility testing
- Performance/load testing
- Docker-based deployment environment
- CI/CD quality checks

### 6.2 Out-of-Scope

The following are not part of the current project unless added as future enhancements:

- Recruitment/Applicant Tracking System
- Employee performance appraisal
- Employee training management
- Benefits administration
- Full accounting/ERP functionality
- Biometric hardware integration
- Government tax-filing integration
- External payroll-provider integration

Defining these exclusions helps control the scope of an individual project and prevents unnecessary expansion during development.

---

## 7. Major Project Modules

The project is divided into the following major functional areas:

### 7.1 Authentication and Authorization

- User login/logout
- Authentication
- Role-based access
- Protected resources

### 7.2 Employee Management

- Add employees
- View employees
- Update employee information
- Manage employee records
- Employee profiles

### 7.3 Attendance Management

- Record attendance
- View attendance
- Validate attendance records
- Attendance reporting

### 7.4 Leave Management

- Submit leave requests
- Review leave requests
- Approve/reject leave
- Maintain leave history
- Validate leave conditions

### 7.5 Payroll Management

- Manage salary information
- Calculate payroll
- Apply payroll-related rules
- Generate payroll information/reports

### 7.6 Dashboard and Reporting

- Display HR information
- Provide summary information
- Generate/view reports

---

## 8. Technology Plan

The project uses the following technology stack based on the existing implementation:

| Layer | Technology |
|---|---|
| Frontend | React |
| Backend | Django |
| API | Django REST Framework |
| Authentication | JWT |
| Database | MySQL |
| Backend Testing | Django/Python test framework |
| Frontend Testing | JavaScript/React testing tools |
| E2E Testing | Playwright |
| Accessibility Testing | Axe |
| Performance Testing | Locust |
| Containerization | Docker / Docker Compose |
| CI/CD | GitHub Actions |
| Version Control | Git |

The selected technologies support a full-stack web application, REST APIs, automated testing, containerization, and continuous integration.

---

## 9. Resource Planning

### 9.1 Human Resources

This is an **individual project**. No separate development, testing, database, or DevOps team is planned.

The student/developer performs all project responsibilities, including:

- Project planning
- Requirements gathering and analysis
- System analysis
- System and database design
- Frontend development
- Backend development
- API development
- Testing
- Debugging
- Deployment
- Documentation
- Maintenance

### 9.2 Technical Resources

The project requires:

- Personal development computer/workstation
- Python environment
- Node.js environment
- MySQL database environment
- Git/GitHub repository
- Docker
- Browser testing environment
- CI/CD environment
- Internet access for development resources and dependency management

---

## 10. Project Constraints

As an individual academic project, the main constraints are:

- Limited development time
- Single-person workload
- Limited financial and infrastructure resources
- Need to learn or manage multiple technologies independently
- Limited availability of realistic HR test data
- Security requirements for employee information
- Payroll business-rule complexity
- Need to balance development, testing, documentation and academic deadlines
- Limited ability to perform parallel development activities

---

## 11. Risk Management

| Risk | Impact | Likelihood | Mitigation |
|---|---|---|---|
| Limited time as an individual developer | High | High | Prioritize core features and follow a phased schedule |
| Scope creep | High | High | Clearly define in-scope and out-of-scope functionality |
| Development workload becomes too large | High | Medium | Break the project into manageable modules |
| Unauthorized access | High | Medium | Authentication, authorization and security testing |
| Incorrect payroll calculation | High | Medium | Unit, integration and regression testing |
| Data loss or corruption | High | Low/Medium | Database backups, validation and recovery procedures |
| API failure | Medium | Medium | Input validation, error handling and integration testing |
| Performance degradation | Medium | Medium | Load and performance testing |
| Vulnerable dependencies | High | Medium | Dependency review and regular updates |
| Deployment failure | Medium | Medium | CI/CD checks and recovery procedures |
| Regression after changes | High | Medium | Automated regression and end-to-end tests |
| Lack of realistic test data | Medium | Medium | Create controlled/synthetic test data while protecting sensitive information |

---

## 12. Development Approach

The project follows a structured SDLC while allowing iterative development because it is an individual academic project.

The planned lifecycle is:

```text
Planning
   ↓
Requirements Analysis
   ↓
System Analysis
   ↓
System Design
   ↓
Implementation
   ↓
Integration
   ↓
Testing
   ↓
Deployment
   ↓
Maintenance
```

The developer may move iteratively between implementation and testing when defects or requirement changes are identified.

Testing is not treated only as the final activity. Testing is performed during development to identify and correct defects early.

---

## 13. High-Level Project Schedule

| SDLC Phase | Main Activity | Expected Output |
|---|---|---|
| Planning | Define project goals, scope, resources and risks | Project plan |
| Requirements Analysis | Identify functional and non-functional requirements | Requirements specification |
| System Analysis | Analyze users, workflows and data | Analysis models |
| System Design | Design architecture, database, APIs and UI | Design specification |
| Implementation | Develop frontend, backend and database | Working modules |
| Integration | Connect frontend, backend and database | Integrated application |
| Testing | Execute functional, security, regression, E2E and performance tests | Test results |
| Deployment | Prepare and deploy application | Deployable system |
| Maintenance | Fix defects and improve the system | Updated releases |

The schedule is adjusted according to the student's academic timeline and workload.

---

## 14. Expected Deliverables

The individual project is expected to produce:

1. Working HR Management System
2. Backend REST APIs
3. Frontend application
4. Database
5. Authentication and authorization system
6. Employee management module
7. Attendance module
8. Leave module
9. Payroll module
10. Dashboard and reporting functionality
11. Automated test suites
12. End-to-end tests
13. Accessibility tests
14. Performance tests
15. Docker configuration
16. CI/CD configuration
17. SDLC documentation
18. Deployment documentation
19. Maintenance documentation

---

## 15. Success Criteria

The project will be considered successful when:

- Core HR workflows operate correctly.
- Users can access only the functionality permitted by their roles.
- Employee, attendance, leave and payroll information is handled consistently.
- Payroll calculations satisfy the defined business rules.
- Automated tests pass the required quality checks.
- Frontend and backend components work correctly together.
- End-to-end workflows operate successfully.
- The application can be built and deployed using the documented process.
- The project documentation accurately describes the implemented system.
- The system can be maintained and extended without unnecessarily breaking existing functionality.

---

## 16. Planning-Stage Gap Analysis

The existing HRMS repository contains substantial implementation, testing, deployment and CI/CD work. However, the Planning stage was not previously separated into a formal SDLC planning document.

This document formalizes the Planning stage by defining:

- Project type
- Project purpose
- Problem statement
- Objectives
- Stakeholders
- Scope
- Out-of-scope functionality
- Major modules
- Technology stack
- Individual developer responsibilities
- Technical resources
- Constraints
- Risks and mitigation
- Development approach
- High-level schedule
- Expected deliverables
- Success criteria

### Planning Status

**Planning Stage: Completed**

The next SDLC stage is **Requirements Analysis**.
