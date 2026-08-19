import { describe, expect, it, beforeEach, vi } from 'vitest';
import api from '../services/api';

beforeEach(() => { localStorage.clear(); vi.restoreAllMocks(); });

describe('API client', () => {
  it('adds access token to outgoing requests', async () => {
    localStorage.setItem('access', 'abc');
    const config = { headers: {} };
    const fulfilled = api.interceptors.request.handlers[0].fulfilled;
    const result = await fulfilled(config);
    expect(result.headers.Authorization).toBe('Bearer abc');
  });
  it('leaves authorization unset without an access token', async () => {
    const config = { headers: {} };
    const fulfilled = api.interceptors.request.handlers[0].fulfilled;
    const result = await fulfilled(config);
    expect(result.headers.Authorization).toBeUndefined();
  });
});
