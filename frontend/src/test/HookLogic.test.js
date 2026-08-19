import { renderHook, act } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import useAlert from '../hooks/useAlert';
import useFormState from '../hooks/useFormState';


describe('Hook logic', () => {
  it('opens and closes alerts', () => { const { result } = renderHook(() => useAlert()); act(() => result.current.showAlert('success', 'Done')); expect(result.current.alert).toMatchObject({ show: true, type: 'success', message: 'Done' }); act(() => result.current.closeAlert()); expect(result.current.alert.show).toBe(false); });
  it('manages form state', () => { const { result } = renderHook(() => useFormState({ name: '' })); act(() => result.current.handleChange({ target: { name: 'name', value: 'John' } })); expect(result.current.formData.name).toBe('John'); });
});
