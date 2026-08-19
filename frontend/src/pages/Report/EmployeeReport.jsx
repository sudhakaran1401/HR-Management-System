import BaseReport from "../../components/report/BaseReport";
import { employeeColumns } from "../../config/columns/EmployeeColumns";
import { getEmployees, downloadEmployeeCSV, downloadEmployeePDF, } from "../../services/EmployeeService";

const EmployeeReport = () => (
  <BaseReport
    title="Employee Report"
    service={getEmployees}
    dateField="joining_date"
    hasEmployee={false}
    moduleName="Employee"
    columns={employeeColumns(false)}
    csvAction={downloadEmployeeCSV}
    pdfAction={downloadEmployeePDF}
    buildReport={(records) => {
      const departmentCounts = {};

      records.forEach((emp) => {
        const department =
          emp.department?.department_name ||
          emp.department?.name ||
          emp.department ||
          "Unknown";

        departmentCounts[department] =
          (departmentCounts[department] || 0) + 1;
      });

      return {
        chartTitle: "Joining Chart",

        summaryCards: [],

        chart: {
          type: "bar",

          data: {
            labels: Object.keys(departmentCounts),

            datasets: [
              {
                label: "Employees",

                data: Object.values(departmentCounts),

                backgroundColor: "#0d6efd",

                borderWidth: 1,
              },
            ],
          },
        },
      };
    }}
  />
);

export default EmployeeReport;