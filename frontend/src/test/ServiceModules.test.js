import { describe, expect, it, vi, beforeEach } from 'vitest';
import * as Attendance from '../services/AttendanceService';
import * as Employee from '../services/EmployeeService';
import * as Leave from '../services/LeaveRequestService';
import * as Payroll from '../services/PayrollService';
import api from '../services/api';

vi.mock('../services/api', () => ({ default: { get: vi.fn(), post: vi.fn(), put: vi.fn(), delete: vi.fn() } }));
vi.mock('../services/CrudService', () => ({ CrudService: () => ({ getAll: vi.fn(), getById: vi.fn(), create: vi.fn(), update: vi.fn(), remove: vi.fn(), download: vi.fn().mockResolvedValue(undefined) }) }));
beforeEach(() => vi.clearAllMocks());

describe('Attendance service', () => {
  it('gets calendar events', async () => { api.get.mockResolvedValue({ data: [{ id: 1 }] }); await expect(Attendance.getAttendanceCalendarEvents()).resolves.toEqual([{ id: 1 }]); expect(api.get).toHaveBeenCalledWith('api/attendance/calendar-events/'); });
});
describe('Employee service', () => {
  it('gets current employee', async () => { api.get.mockResolvedValue({ data: { id: 1 } }); await expect(Employee.getCurrentEmployee()).resolves.toEqual({ id: 1 }); expect(api.get).toHaveBeenCalledWith('api/employees/me/'); });
});
describe('Leave service', () => {
  it('gets own leave balance', async () => { api.get.mockResolvedValue({ data: { total: 4 } }); await Leave.getLeaveBalance(); expect(api.get).toHaveBeenCalledWith('api/leave/balance/'); });
  it('gets employee leave balance', async () => { api.get.mockResolvedValue({ data: {} }); await Leave.getLeaveBalance(7); expect(api.get).toHaveBeenCalledWith('api/leave/balance/7/'); });
  it('approves and rejects leave', async () => { api.post.mockResolvedValue({}); await Leave.approveLeave(2); await Leave.rejectLeave(2); expect(api.post).toHaveBeenNthCalledWith(1, 'api/leave/2/approve/'); expect(api.post).toHaveBeenNthCalledWith(2, 'api/leave/2/reject/'); });
});
describe('Payroll service', () => {
  it('downloads a payslip through crud download', async () => { await expect(Payroll.downloadPayslip(8)).resolves.not.toThrow(); });
});
