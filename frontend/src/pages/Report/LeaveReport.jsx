import BaseReport from "../../components/report/BaseReport";
import { buildLeaveStatistics, } from "../../utils/reportStatistics";
import { buildLeaveSummaryCards, } from "../../utils/reportSummaryCards";
import { leaveColumns } from "../../config/columns/LeaverequestColumns";
import { getLeaves, downloadLeaveCSV, downloadLeavePDF, } from "../../services/LeaveRequestService";

const LeaveReport = () => (
  <BaseReport
    title="Leave Report"
    service={getLeaves}
    dateField="applied_at"
    moduleName="Leave"
    columns={leaveColumns(false)}
    csvAction={downloadLeaveCSV}
    pdfAction={downloadLeavePDF}
    buildReport={(records) => {
      const stats = buildLeaveStatistics(records);

      return {
        chartTitle: "Leave Statistics",

        summaryCards: buildLeaveSummaryCards(stats),

        chart: {
          type: "bar",

          data: {
            labels: [
              "Approved",
              "Pending",
              "Rejected",
            ],

            datasets: [
              {
                label: "Leave Requests",

                data: [
                  stats.approved,
                  stats.pending,
                  stats.rejected,
                ],

                backgroundColor: [
                  "#198754",
                  "#ffc107",
                  "#dc3545",
                ],

                borderRadius: 5,
              },
            ],
          },
        },
      };
    }}
  />
);

export default LeaveReport;