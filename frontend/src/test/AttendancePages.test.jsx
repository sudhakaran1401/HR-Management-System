import { render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { MemoryRouter } from 'react-router-dom';
import Attendance from '../pages/List/Attendance';
import AttendanceForm from '../pages/Form/AttendanceForm';
import AttendanceCalendar from '../pages/Views/AttendanceCalendar';

vi.mock('../components/list/CrudListPage', () => ({ default: ({ title, buttonText }) => <div><h1>{title}</h1><button>{buttonText}</button></div> }));
vi.mock('../services/AttendanceService', () => ({ getAttendance: vi.fn() }));
vi.mock('../config/columns/AttendanceColumns', () => ({ attendanceColumns: [] }));
vi.mock('../hooks/Employee/useEmployee', () => ({ default: () => ({ loggedEmployee: { id: 1 } }) }));
vi.mock('../utils/loadEmployeeRecords', () => ({ default: vi.fn() }));
vi.mock('../services/api', () => ({ default: { get: vi.fn(), post: vi.fn(), put: vi.fn() } }));
vi.mock('../layouts/FormLayout', () => ({ default: ({ title, children }) => <div><h1>{title}</h1>{children}</div> }));

describe('Attendance pages', () => {
  it('renders attendance list title', () => { render(<MemoryRouter><Attendance /></MemoryRouter>); expect(screen.getByText('Attendance Records')).toBeInTheDocument(); });
  it('exports attendance form', () => expect(AttendanceForm).toBeTruthy());
  it('exports attendance calendar', () => expect(AttendanceCalendar).toBeTruthy());
});
