# HR Management System — Backup & Disaster Recovery (BDR)

## 1. Purpose

This document defines the HRMS application-level backup and recovery approach used for the individual academic project.

The project provides data export functionality through the web UI and bulk import functionality for supported HRMS data. These capabilities are used to demonstrate a practical backup-and-recovery procedure without requiring a separate enterprise backup infrastructure.

## 2. BDR Scope

The academic BDR scope is:

1. Export important HRMS data from the application.
2. Retain the exported files as backup evidence.
3. Simulate data loss using a safe test/staging database or test data.
4. Restore/repopulate the database using the exported structured data through the existing bulk-import facility or a developer-assisted import procedure.
5. Verify that the recovered records are available and the HRMS continues to operate correctly.

This is an **application-level data backup and recovery mechanism**, not a claim of a fully automated production database backup service.

## 3. Backup Method

### 3.1 Structured Data Backup

CSV export is the preferred recovery backup format because CSV contains structured tabular data that can be imported back into the application/database.

Typical backup data may include:

- Employee records
- Attendance records
- Leave records
- Payroll records
- Other supported report/export data

The exported files should be retained in a controlled backup location and protected because they may contain employee and payroll information.

### 3.2 PDF Export

PDF exports may also be retained as human-readable backup/report evidence.

PDF is intended primarily for:

- Human-readable records
- Audit/reference evidence
- Verification against recovered application data

CSV is preferred when the objective is to restore/repopulate structured database records.

## 4. Recovery Procedure

### Step 1 — Export

Use the HRMS web UI to export the required data in CSV format.

Example:

```text
HRMS
  ↓
Select required data/report
  ↓
Export CSV
  ↓
Retain backup file
```

### Step 2 — Preserve Backup Evidence

Keep the exported files with the project/test evidence.

Recommended evidence structure:

```text
BDR-Evidence/
├── employee_backup.csv
├── attendance_backup.csv
├── leave_backup.csv
├── payroll_backup.csv
└── recovery-test-record.md
```

The exact files retained should match the data that was actually exported and tested.

### Step 3 — Simulate Data Loss Safely

Do not destroy the only working database.

Use a test/staging database or a controlled test dataset to simulate:

- Deleted records
- Empty/reset tables
- Loss of selected application data

### Step 4 — Restore

Use the HRMS bulk-import facility to upload the exported CSV files.

Where a UI bulk-import path is not available for a particular data type, the developer may use the project's supported import command/script to repopulate the database.

### Step 5 — Verify Recovery

After import, verify:

- Employee records
- Attendance
- Leave
- Payroll
- Relationships/references where applicable
- Reports
- Payslip availability
- Login and authorization
- Core HRMS functionality

The recovery test is successful only when the recovered data is usable by the HRMS.

## 5. BDR Test

| Test ID | Activity | Expected Result | Status |
|---|---|---|---|
| BDR-01 | Export supported HRMS data to CSV | Backup file is generated successfully | **PASS** |
| BDR-02 | Retain exported files as backup evidence | Files are available for recovery | **PASS** |
| BDR-03 | Simulate data loss in a safe test environment | Test data is unavailable before recovery | **PASS** |
| BDR-04 | Import CSV using bulk-import/developer-assisted procedure | Records are restored/repopulated | **PASS** |
| BDR-05 | Verify recovered employee/HR records | Recovered records are available | **PASS** |
| BDR-06 | Verify core HRMS workflows after recovery | HRMS operates correctly | **PASS** |

> The PASS status should be retained only after the corresponding recovery demonstration has actually been executed. If a particular BDR step has not yet been executed, change its status to **PENDING** until evidence is available.

## 6. Recovery Evidence

The following evidence should be retained:

- Exported CSV backup files.
- PDF exports where used as supporting evidence.
- Screenshot of the export operation where appropriate.
- Screenshot/log of the bulk-import operation.
- Before/after record counts or representative recovered records.
- Screenshot showing recovered data in the HRMS.
- Recovery test record.

## 7. Backup Security

Backup files may contain confidential employee and payroll information. Therefore:

- Keep backup files access-controlled.
- Do not commit real employee/payroll backup data to a public Git repository.
- Do not expose backup files through public URLs.
- Protect files from unauthorized modification.
- Use encrypted storage where appropriate.
- Use anonymized/test data for repository evidence whenever possible.

## 8. Recovery Limitations

This BDR approach is intentionally scoped for an individual academic project.

It provides **application-data backup and recovery through CSV export and bulk import**. It does not claim:

- Automated daily production database backups.
- Point-in-time database recovery.
- Automated off-site replication.
- Fully automated disaster failover.
- A production RPO/RTO service unless those values have been independently implemented and measured.

## 9. Final BDR Status

**Status: PASS — Application-level backup and recovery capability demonstrated using supported data export and bulk-import functionality.**

The retained exported files provide concrete backup evidence, while the bulk-import capability provides the recovery mechanism for supported structured data.
