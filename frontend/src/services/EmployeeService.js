import { CrudService } from "./CrudService";
import api from "./api";
import { downloadFile } from "./DownloadService";

const BASE_URL = "api/employees/";

const crud = CrudService(BASE_URL);

export const getEmployees = crud.getAll;
export const getEmployee = crud.getById;
export const createEmployee = crud.create;
export const updateEmployee = crud.update;
export const deleteEmployee = crud.remove;

export const getCurrentEmployee = async () => {
  const { data } = await api.get(`${BASE_URL}me/`);
  return data;
};


export const downloadEmployeeCSV = (params) =>
  crud.download( "download/csv", params, "Employee_Report.csv", "text/csv" );

export const downloadEmployeePDF = (params) =>
  crud.download( "download/pdf", params, "Employee_Report.pdf", "application/pdf" );