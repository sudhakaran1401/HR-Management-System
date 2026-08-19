import { describe, expect, it } from 'vitest';
import { filterReportData } from '../utils/filterReportData';
import { formatDate, formatDateTime, formatMonth, formatTime } from '../utils/formatters';
import { mergeEmployeeDetails } from '../utils/mergeEmployeeDetails';
import { buildAttendanceStatistics, buildLeaveStatistics } from '../utils/reportStatistics';
import { buildAttendanceSummaryCards, buildLeaveSummaryCards } from '../utils/reportSummaryCards';

const records = [
  { id: 1, employee: 1, date: '2026-08-10', status: 'Present' },
  { id: 2, employee: 2, date: '2026-07-10', status: 'Leave' },
  { id: 3, employee: 1, date: '2026-08-11', status: 'Holiday' },
];

describe('Report utilities', () => {
  it('filters by employee, month and year', () => { expect(filterReportData({ records, dateField: 'date', month: 8, year: 2026, employee: 1 })).toHaveLength(2); });
  it('formats common date values', () => { expect(formatDate('2026-08-10')).toMatch(/Aug/); expect(formatMonth('2026-08-10')).toMatch(/Aug/); expect(formatTime('13:30:00')).toMatch(/01:30/); expect(formatDateTime('2026-08-10T13:30:00')).toMatch(/Aug/); });
  it('returns dash for empty date values', () => { expect(formatDate()).toBe('-'); expect(formatMonth()).toBe('-'); expect(formatTime()).toBe('-'); expect(formatDateTime()).toBe('-'); });
  it('merges employee details', () => { const out = mergeEmployeeDetails([{ employee: 1 }], [{ id: 1, name: 'John' }]); expect(out[0].employeeDetails.name).toBe('John'); });
  it('calculates attendance statistics', () => { expect(buildAttendanceStatistics(records)).toEqual({ present: 1, leave: 1, holiday: 1 }); });
  it('calculates leave statistics', () => { expect(buildLeaveStatistics([{ status: 'APPROVED' }, { status: 'PENDING' }, { status: 'REJECTED' }])).toEqual({ totalApplied: 3, approved: 1, pending: 1, rejected: 1 }); });
  it('builds summary cards', () => { expect(buildAttendanceSummaryCards({ present: 2, leave: 1, holiday: 3 })).toHaveLength(3); expect(buildLeaveSummaryCards({ totalApplied: 4, approved: 2, pending: 1, rejected: 1 })).toHaveLength(4); });
});
