import { describe, expect, it, vi, beforeEach } from 'vitest';
import { CrudService } from '../services/CrudService';
import api from '../services/api';

vi.mock('../services/api', () => ({ default: { get: vi.fn(), post: vi.fn(), put: vi.fn(), delete: vi.fn() } }));
vi.mock('../services/DownloadService', () => ({ downloadFile: vi.fn() }));

beforeEach(() => vi.clearAllMocks());

describe('CrudService', () => {
  const crud = CrudService('api/test/');
  it('gets all records', async () => { api.get.mockResolvedValue({ data: [1] }); expect(await crud.getAll()).toEqual([1]); expect(api.get).toHaveBeenCalledWith('api/test/'); });
  it('gets a record by id', async () => { api.get.mockResolvedValue({ data: { id: 3 } }); await crud.getById(3); expect(api.get).toHaveBeenCalledWith('api/test/3/'); });
  it('creates a record', async () => { api.post.mockResolvedValue({ data: {} }); await crud.create({ name: 'x' }); expect(api.post).toHaveBeenCalledWith('api/test/create/', { name: 'x' }); });
  it('updates a record', async () => { api.put.mockResolvedValue({ data: {} }); await crud.update(2, { name: 'y' }); expect(api.put).toHaveBeenCalledWith('api/test/2/update/', { name: 'y' }); });
  it('deletes a record', async () => { api.delete.mockResolvedValue({}); await crud.remove(2); expect(api.delete).toHaveBeenCalledWith('api/test/2/delete/'); });
});
