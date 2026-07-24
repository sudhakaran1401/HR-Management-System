
import { CrudService } from "./CrudService";
import api from "./api";
import { downloadFile } from "./DownloadService";

const BASE_URL = "api/payroll/";

const crud = CrudService(BASE_URL);

export const getPayrolls = crud.getAll;
export const getPayrollById = crud.getById;
export const createPayroll = crud.create;
export const updatePayroll = crud.update;
export const deletePayroll = crud.remove;

export const downloadPayrollCSV = (params) =>
  crud.download( "download/csv", params, "Payroll_Report.csv", "text/csv" );

export const downloadPayrollPDF = (params) =>
  crud.download( "download/pdf", params, "Payroll_Report.pdf", "application/pdf" );

export const downloadPayslip = (id) =>
  crud.download( `${id}/payslip/`, undefined, "Payslip.pdf", "application/pdf" );