import { render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { MemoryRouter } from 'react-router-dom';
import Employees from '../pages/List/Employees';
import EmployeeView from '../pages/Views/EmployeeView';
import EmployeeForm from '../pages/Form/EmployeeForm';
import EmployeeDelete from '../pages/Form/EmployeeDelete';

vi.mock('../components/list/CrudListPage', () => ({ default: ({ title, buttonText }) => <div><h1>{title}</h1><button>{buttonText}</button></div> }));
vi.mock('../services/EmployeeService', () => ({ getEmployees: vi.fn() }));
vi.mock('../config/columns/EmployeeColumns', () => ({ employeeColumns: () => [] }));
vi.mock('../hooks/Employee/useEmployee', () => ({ default: () => ({ loggedEmployee: { id: 1, department: 'HR' } }) }));
vi.mock('../hooks/Employee/useCurrentEmployee', () => ({ default: () => ({ employee: { id: 1, name: 'John' }, loading: false, error: null }) }));
vi.mock('../hooks/Employee/useLoggedEmployee', () => ({ default: () => ({ id: 1, department: 'HR' }) }));
vi.mock('../services/api', () => ({ default: { get: vi.fn(), post: vi.fn(), put: vi.fn(), delete: vi.fn() } }));
vi.mock('../components/PageHeader', () => ({ default: ({ title }) => <h1>{title}</h1> }));

vi.mock('../layouts/FormLayout', () => ({ default: ({ title, children }) => <div><h1>{title}</h1>{children}</div> }));

describe('Employee pages', () => {
  it('renders employee list', () => { render(<MemoryRouter><Employees /></MemoryRouter>); expect(screen.getByText('Employees')).toBeInTheDocument(); });
  it('loads employee view module', () => { expect(EmployeeView).toBeTruthy(); });
  it('loads employee form module', () => { expect(EmployeeForm).toBeTruthy(); });
  it('loads employee delete module', () => { expect(EmployeeDelete).toBeTruthy(); });
});
