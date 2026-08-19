import { render, screen } from '@testing-library/react';
import { describe, expect, it, vi, beforeEach } from 'vitest';
import { MemoryRouter } from 'react-router-dom';
import HRDashboard from '../pages/Dashboard/HRDashboard';
import EmployeeDashboard from '../pages/Dashboard/EmployeeDashboard';

vi.mock('../hooks/useDashboard', () => ({ default: ({ initialData }) => ({ alert: { show: false }, closeAlert: vi.fn(), data: initialData, year: '', month: '', day: '', setYear: vi.fn(), setMonth: vi.fn(), setDay: vi.fn(), dashboardMode: 'HR', isHR: true, fetchDashboard: vi.fn(), handleReset: vi.fn(), handleRoleToggle: vi.fn() }) }));
vi.mock('../components/dashboard/DashboardPage', () => ({ default: ({ title, children }) => <section><h1>{title}</h1>{children}</section> }));
vi.mock('../components/dashboard/KPIGrid', () => ({ default: () => <div>KPI Grid</div> }));
vi.mock('../components/dashboard/DashboardCharts', () => ({ default: () => <div>Charts</div> }));
vi.mock('../components/dashboard/ReportButtons', () => ({ default: () => <div>Reports</div> }));
vi.mock('../components/dashboard/EmptyDashboardCard', () => ({ default: () => <div>No dashboard data</div> }));
vi.mock('../components/dashboard/ProfileCard', () => ({ default: () => <div>Profile</div> }));
vi.mock('../components/dashboard/DashboardCard', () => ({ KPICard: () => <div>KPI</div>, AttendanceCard: () => <div>Attendance</div>, LeaveCard: () => <div>Leave</div> }));
vi.mock('../services/api', () => ({ default: { get: vi.fn().mockResolvedValue({ data: {} }) } }));

beforeEach(() => vi.clearAllMocks());

describe('Dashboards', () => {
  it('renders HR dashboard title', () => { render(<MemoryRouter><HRDashboard /></MemoryRouter>); expect(screen.getByText('HR Dashboard')).toBeInTheDocument(); });
  it('renders employee dashboard title', () => { render(<MemoryRouter><EmployeeDashboard /></MemoryRouter>); expect(screen.getByText('Employee Dashboard')).toBeInTheDocument(); });
});
