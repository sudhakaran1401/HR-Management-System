import { render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { MemoryRouter } from 'react-router-dom';
import Payroll from '../pages/List/Payroll';
import PayrollForm from '../pages/Form/PayrollForm';
import PayslipView from '../pages/Views/PayslipView';

vi.mock('../components/list/CrudListPage', () => ({ default: ({ title }) => <h1>{title}</h1> }));
vi.mock('../services/PayrollService', () => ({ getPayrolls: vi.fn(), downloadPayslip: vi.fn() }));
vi.mock('../config/columns/PayrollColumns', () => ({ payrollColumns: () => [] }));
vi.mock('../utils/loadEmployeeRecords', () => ({ default: vi.fn() }));
vi.mock('../hooks/Employee/useEmployee', () => ({ default: () => ({ loggedEmployee: { id: 1 } }) }));
vi.mock('../layouts/FormLayout', () => ({ default: ({ title, children }) => <div><h1>{title}</h1>{children}</div> }));
vi.mock('../services/api', () => ({ default: { get: vi.fn(), post: vi.fn(), put: vi.fn() } }));

describe('Payroll pages', () => {
  it('renders payroll title', () => { render(<MemoryRouter><Payroll /></MemoryRouter>); expect(screen.getByText('Payroll History')).toBeInTheDocument(); });
  it('exports payroll form', () => expect(PayrollForm).toBeTruthy());
  it('exports payslip view', () => expect(PayslipView).toBeTruthy());
});
