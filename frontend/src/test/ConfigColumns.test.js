import { describe, expect, it } from 'vitest';
import { employeeColumns } from '../config/columns/EmployeeColumns';
import { attendanceColumns } from '../config/columns/AttendanceColumns';
import { leaveColumns } from '../config/columns/LeaverequestColumns';
import { payrollColumns } from '../config/columns/PayrollColumns';
import { departments } from '../config/constants/departments';
import { REPORT_YEARS } from '../config/constants/reportYears';

describe('Frontend configuration', () => {
  it('provides employee columns', () => expect(employeeColumns(false, () => {})).toBeTruthy());
  it('provides attendance columns', () => expect(attendanceColumns).toBeTruthy());
  it('provides leave columns', () => expect(leaveColumns({ isHRPage: true, isMyLeavePage: false })).toBeTruthy());
  it('provides payroll columns', () => expect(payrollColumns(false)).toBeTruthy());
  it('provides department constants', () => expect(departments.length).toBeGreaterThan(0));
  it('provides report years', () => expect(REPORT_YEARS.length).toBeGreaterThan(0));
});
