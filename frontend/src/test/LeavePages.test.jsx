import { render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { MemoryRouter } from 'react-router-dom';
import Leaverequest from '../pages/List/Leaverequest';
import LeaveForm from '../pages/Form/LeaveForm';

vi.mock('../components/list/CrudListPage', () => ({ default: ({ title }) => <h1>{title}</h1> }));
vi.mock('../services/LeaveRequestService', () => ({ getLeaves: vi.fn(), approveLeave: vi.fn(), rejectLeave: vi.fn() }));
vi.mock('../config/columns/LeaverequestColumns', () => ({ leaveColumns: () => [] }));
vi.mock('../utils/loadEmployeeRecords', () => ({ default: vi.fn() }));
vi.mock('../hooks/Employee/useLoggedEmployee', () => ({ default: () => ({ id: 1 }) }));
vi.mock('../layouts/FormLayout', () => ({ default: ({ title, children }) => <div><h1>{title}</h1>{children}</div> }));

describe('Leave pages', () => {
  it('renders leave requests title', () => { render(<MemoryRouter><Leaverequest /></MemoryRouter>); expect(screen.getByText('Leave Requests')).toBeInTheDocument(); });
  it('exports leave form', () => expect(LeaveForm).toBeTruthy());
});
