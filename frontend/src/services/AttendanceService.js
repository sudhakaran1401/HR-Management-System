
import { CrudService } from "./CrudService";
import api from "./api";
import { downloadFile } from "./DownloadService";

const BASE_URL = "api/attendance/";

const crud = CrudService(BASE_URL);

export const getAttendance = crud.getAll;
export const getAttendanceById = crud.getById;
export const createAttendance = crud.create;
export const updateAttendance = crud.update;
export const deleteAttendance = crud.remove;


export const getAttendanceCalendarEvents = async () => {
    const response = await api.get(`${BASE_URL}calendar-events/`);
    return response.data;
};

export const downloadAttendanceCSV = (params) =>
  crud.download( "download/csv/", params, "Attendance_Report.csv", "text/csv" );

export const downloadAttendancePDF = (params) =>
  crud.download( "download/pdf/", params, "Attendance_Report.pdf", "application/pdf" );