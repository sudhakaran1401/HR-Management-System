import BaseReport from "../../components/report/BaseReport";
import { buildAttendanceStatistics } from "../../utils/reportStatistics";
import { buildAttendanceSummaryCards } from "../../utils/reportSummaryCards";
import { attendanceColumns } from "../../config/columns/AttendanceColumns";
import { getAttendance, downloadAttendanceCSV, downloadAttendancePDF } from "../../services/AttendanceService";

const AttendanceReport = () => (
  <BaseReport
    title="Attendance Report"
    service={getAttendance}
    dateField="date"
    moduleName="Attendance"
    columns={attendanceColumns}
    csvAction={downloadAttendanceCSV}
    pdfAction={downloadAttendancePDF}
    buildReport={(records) => {
      const stats = buildAttendanceStatistics(records);

      return {
        chartTitle: "Attendance Statistics",

        summaryCards: buildAttendanceSummaryCards(stats),

        chart: {
          type: "pie",

          data: {
            labels: [
              "Present",
              "Leave",
              "Holiday",
            ],

            datasets: [
              {
                label: "Attendance",

                data: [
                  stats.present,
                  stats.leave,
                  stats.holiday,
                ],

                backgroundColor: [
                  "#198754",
                  "#dc3545",
                  "#0dcaf0",
                ],

                borderWidth: 1,
              },
            ],
          },
        },
      };
    }}
  />
);

export default AttendanceReport;