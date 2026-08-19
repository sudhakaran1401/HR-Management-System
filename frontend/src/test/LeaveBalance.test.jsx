import { render, screen, waitFor } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { MemoryRouter } from 'react-router-dom';
import LeaveBalance from '../pages/Dashboard/LeaveBalance';
import { getLeaveBalance } from '../services/LeaveRequestService';

vi.mock('../services/LeaveRequestService', () => ({ getLeaveBalance: vi.fn() }));
vi.mock('../hooks/Employee/useLoggedEmployee', () => ({ default: () => ({ department: 'IT', id: 1 }) }));
vi.mock('../components/Loader', () => ({ default: () => <div>Loading</div> }));
vi.mock('../components/PageHeader', () => ({ default: ({ title }) => <h1>{title}</h1> }));
vi.mock('../components/report/SummaryCards', () => ({ default: ({ cards }) => <div>{cards.map(c => <span key={c.title}>{c.title}:{c.value}</span>)}</div> }));
vi.mock('../components/dashboard/LeaveSummaryCard', () => ({ default: ({ balance }) => <div>{balance.employee}</div> }));

describe('Leave balance', () => {
  it('loads and displays balance', async () => {
    getLeaveBalance.mockResolvedValue({ employee: 'John', total: 4, approved: 2, pending: 1, rejected: 1 });
    render(<MemoryRouter initialEntries={['/leave-balance']}><LeaveBalance /></MemoryRouter>);
    await waitFor(() => expect(screen.getByText('Leave Balance')).toBeInTheDocument());
    expect(screen.getByText('John')).toBeInTheDocument();
  });
});
