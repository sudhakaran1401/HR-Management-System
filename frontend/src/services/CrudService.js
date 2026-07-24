import api from "./api";
import { downloadFile } from "./DownloadService";

export const CrudService = (baseUrl) => ({
  getAll: async () => {
    const { data } = await api.get(baseUrl);
    return data;
  },

  getById: async (id) => {
    const { data } = await api.get(`${baseUrl}${id}/`);
    return data;
  },

  create: (payload) =>
    api.post(`${baseUrl}create/`, payload),

  update: (id, payload) =>
    api.put(`${baseUrl}${id}/update/`, payload),

  remove: (id) =>
    api.delete(`${baseUrl}${id}/delete/`),

  download: async (endpoint, params, filename, mimeType) => {
    const response = await api.get(`${baseUrl}${endpoint}`, {
      params,
      responseType: "blob",
    });

    downloadFile(response, filename, mimeType);
  }
});