import { describe, expect, it } from 'vitest';
import EmployeeReport from '../pages/Report/EmployeeReport';
import AttendanceReport from '../pages/Report/AttendanceReport';
import LeaveReport from '../pages/Report/LeaveReport';
import PayrollReport from '../pages/Report/PayrollReport';

describe('Report pages', () => {
  it.each([
    ['Employee report', EmployeeReport],
    ['Attendance report', AttendanceReport],
    ['Leave report', LeaveReport],
    ['Payroll report', PayrollReport],
  ])('%s module is available', (_, component) => expect(component).toBeTruthy());
});
