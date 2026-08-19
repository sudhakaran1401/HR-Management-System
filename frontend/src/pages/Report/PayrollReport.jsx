import BaseReport from "../../components/report/BaseReport";
import { payrollColumns } from "../../config/columns/PayrollColumns";
import { getPayrolls, downloadPayrollCSV, downloadPayrollPDF, downloadPayslip, } from "../../services/PayrollService";

const PayrollReport = () => {
  const handlePdf = async (id) => {
    try {
      await downloadPayslip(id);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <BaseReport
      title="Payroll Report"
      service={getPayrolls}
      dateField="pay_month"
      moduleName="Payroll"
      columns={payrollColumns(false)}
      csvAction={downloadPayrollCSV}
      pdfAction={downloadPayrollPDF}
      transformRecords={(records) =>
        records.map((payroll) => ({
          ...payroll,
          onPdf: handlePdf,
        }))
      }
      buildReport={(records) => {
        const grouped = {};

        records.forEach((payroll) => {
          const date = new Date(payroll.pay_month);

          const key = `${date.getFullYear()}-${String(
            date.getMonth() + 1
          ).padStart(2, "0")}`;

          grouped[key] =
            (grouped[key] || 0) +
            Number(payroll.stored_net_pay);
        });

        const sortedKeys =
          Object.keys(grouped).sort();

        return {
          chartTitle: "Salary Trend",

          summaryCards: [],

          chart: {
            type: "line",

            data: {
              labels: sortedKeys.map((key) => {
                const [year, month] = key.split("-");

                return new Date(
                  year,
                  month - 1
                ).toLocaleDateString("en-US", {
                  month: "short",
                  year: "numeric",
                });
              }),

              datasets: [
                {
                  label: "Total Net Pay",

                  data: sortedKeys.map(
                    (key) => grouped[key]
                  ),

                  borderColor: "#0d6efd",

                  backgroundColor: "#0d6efd",

                  tension: 0.3,
                },
              ],
            },
          },
        };
      }}
    />
  );
};

export default PayrollReport;