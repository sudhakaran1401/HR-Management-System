import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, expect, it, beforeEach, vi } from 'vitest';
import { MemoryRouter } from 'react-router-dom';
import Login from '../pages/Main/Login';
import api from '../services/api';

vi.mock('../services/api', () => ({ default: { post: vi.fn(), get: vi.fn() } }));
vi.mock('../components/Navbar', () => ({ default: () => <nav>Navbar</nav> }));
vi.mock('../components/AlertMessage', () => ({ default: ({ message }) => message ? <div>{message}</div> : null }));
vi.mock('../hooks/useAlert', () => ({ default: () => ({ alert: { show: false }, showAlert: vi.fn(), closeAlert: vi.fn() }) }));

const renderLogin = () => render(<MemoryRouter><Login /></MemoryRouter>);

beforeEach(() => { vi.clearAllMocks(); localStorage.clear(); sessionStorage.clear(); });

describe('Login page', () => {
  it('renders username, password and login button', () => {
    renderLogin();
    expect(screen.getByPlaceholderText('Enter username')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Enter password')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Login' })).toBeInTheDocument();
  });

  it('submits credentials to the token endpoint', async () => {
    api.post.mockResolvedValueOnce({ data: { access: 'a', refresh: 'r' } });
    api.get.mockResolvedValueOnce({ data: { id: 1 } });
    api.get.mockResolvedValueOnce({ data: [{ id: 9, user: 1, department: 'IT' }] });
    renderLogin();
    fireEvent.change(screen.getByPlaceholderText('Enter username'), { target: { value: 'john' } });
    fireEvent.change(screen.getByPlaceholderText('Enter password'), { target: { value: 'secret' } });
    fireEvent.click(screen.getByRole('button', { name: 'Login' }));
    await waitFor(() => expect(api.post).toHaveBeenCalledWith('/api/token/', { username: 'john', password: 'secret' }));
  });

  it('stores tokens after successful authentication', async () => {
    api.post.mockResolvedValueOnce({ data: { access: 'access-token', refresh: 'refresh-token' } });
    api.get.mockResolvedValueOnce({ data: { id: 1 } });
    api.get.mockResolvedValueOnce({ data: [{ id: 9, user: 1, department: 'IT' }] });
    renderLogin();
    fireEvent.change(screen.getByPlaceholderText('Enter username'), { target: { value: 'john' } });
    fireEvent.change(screen.getByPlaceholderText('Enter password'), { target: { value: 'secret' } });
    fireEvent.click(screen.getByRole('button', { name: 'Login' }));
    await waitFor(() => {
      expect(localStorage.getItem('access')).toBe('access-token');
      expect(localStorage.getItem('refresh')).toBe('refresh-token');
    });
  });

  it('handles invalid credentials without crashing', async () => {
    api.post.mockRejectedValueOnce(new Error('invalid'));
    renderLogin();
    fireEvent.change(screen.getByPlaceholderText('Enter username'), { target: { value: 'bad' } });
    fireEvent.change(screen.getByPlaceholderText('Enter password'), { target: { value: 'bad' } });
    fireEvent.click(screen.getByRole('button', { name: 'Login' }));
    await waitFor(() => expect(api.post).toHaveBeenCalled());
  });
});
