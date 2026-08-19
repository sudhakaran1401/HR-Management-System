/* globals global */
import { describe, expect, it, vi, beforeEach } from 'vitest';
import { downloadFile } from '../services/DownloadService';

beforeEach(() => {
  vi.restoreAllMocks();
  global.URL.createObjectURL = vi.fn(() => 'blob:url');
  global.URL.revokeObjectURL = vi.fn();
});

describe('downloadFile', () => {
  it('uses the default filename when no disposition is supplied', () => {
    const click = vi.fn();
    vi.spyOn(document, 'createElement').mockReturnValue({ href: '', download: '', click, remove: vi.fn() });
    vi.spyOn(document.body, 'appendChild').mockImplementation(() => {});
    downloadFile({ data: 'x', headers: {} }, 'report.pdf', 'application/pdf');
    expect(click).toHaveBeenCalled();
  });
  it('uses the filename from content disposition', () => {
    const link = { href: '', download: '', click: vi.fn(), remove: vi.fn() };
    vi.spyOn(document, 'createElement').mockReturnValue(link);
    vi.spyOn(document.body, 'appendChild').mockImplementation(() => {});
    downloadFile({ data: 'x', headers: { 'content-disposition': 'attachment; filename="custom.pdf"' } }, 'report.pdf', 'application/pdf');
    expect(link.download).toBe('custom.pdf');
  });
});
