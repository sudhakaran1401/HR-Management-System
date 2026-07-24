
import { CrudService } from "./CrudService";
import api from "./api";
import { downloadFile } from "./DownloadService";

const BASE_URL = "api/leave/";

const crud = CrudService(BASE_URL);

export const getLeaves = crud.getAll;
export const getLeave = crud.getById;
export const createLeave = crud.create;
export const updateLeave = crud.update;
export const deleteLeave = crud.remove;

export const getLeaveBalance = async (employeeId = null) => {
  const url = employeeId
    ? `${BASE_URL}balance/${employeeId}/`
    : `${BASE_URL}balance/`;

  const { data } = await api.get(url);
  return data;
};

export const approveLeave = (id) =>
    api.post(`${BASE_URL}${id}/approve/`);

export const rejectLeave = (id) =>
    api.post(`${BASE_URL}${id}/reject/`);

export const downloadLeaveCSV = (params) =>
  crud.download( "download/csv/", params, "Leave_Report.csv", "text/csv" );

export const downloadLeavePDF = (params) =>
  crud.download( "download/pdf/", params, "Leave_Report.pdf", "application/pdf" );