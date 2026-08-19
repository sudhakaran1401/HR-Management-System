import { render, screen, fireEvent } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import StatusBadge from '../components/StatusBadge';
import ThemeToggle from '../components/ThemeToggle';
import AlertMessage from '../components/AlertMessage';


describe('Basic UI components', () => {
  it('renders known and fallback statuses', () => { const { rerender } = render(<StatusBadge status="Present" />); expect(screen.getByText('Present')).toBeInTheDocument(); rerender(<StatusBadge status="UNKNOWN" />); expect(screen.getByText('UNKNOWN')).toBeInTheDocument(); rerender(<StatusBadge />); expect(screen.getByText('Not marked')).toBeInTheDocument(); });
  it('toggles theme and persists it', () => { localStorage.clear(); render(<ThemeToggle />); const input = screen.getByRole('checkbox'); fireEvent.click(input); expect(localStorage.getItem('theme')).toBe('dark'); expect(document.body.classList.contains('dark-mode')).toBe(true); });
  it('renders an alert message when shown', () => { render(<AlertMessage show type="danger" message="Something went wrong" onClose={() => {}} />); expect(screen.getByText('Something went wrong')).toBeInTheDocument(); });
});
