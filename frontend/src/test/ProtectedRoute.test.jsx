import { render, screen } from '@testing-library/react';
import { describe, expect, it, beforeEach } from 'vitest';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import ProtectedRoute from '../components/ProtectedRoute';

const renderRoute = () => render(<MemoryRouter initialEntries={['/protected']}><Routes><Route path="/" element={<div>Login</div>} /><Route path="/protected" element={<ProtectedRoute><div>Protected</div></ProtectedRoute>} /></Routes></MemoryRouter>);
beforeEach(() => localStorage.clear());

describe('ProtectedRoute', () => {
  it('redirects when access token is missing', () => { renderRoute(); expect(screen.getByText('Login')).toBeInTheDocument(); });
  it('renders children when access token exists', () => { localStorage.setItem('access', 'token'); renderRoute(); expect(screen.getByText('Protected')).toBeInTheDocument(); });
});
