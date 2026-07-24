import { useParams } from "react-router-dom";

import CrudListPage from "../../components/list/CrudListPage";

import { payrollColumns } from "../../config/columns/PayrollColumns";

import * as PayrollService from "../../services/PayrollService";
import { downloadPayslip } from "../../services/PayrollService";

import loadEmployeeRecords from "../../utils/loadEmployeeRecords";
import useEmployee from "../../hooks/Employee/useEmployee";

const Payroll = () => {
  const { employeeId } = useParams();

  const { loggedEmployee } = useEmployee();

  return (
    <CrudListPage
      title="Payroll History"
      buttonText={({ location }) =>
        location.pathname === "/me/payroll"
          ? null
          : "+ Add Payroll"
      }
      searchPlaceholder="Search payroll..."
      dependencies={[employeeId]}
      columns={({ location }) =>
        payrollColumns(
          location.pathname === "/me/payroll"
        )
      }
      loadData={({
        mergeEmployees,
        showAlert,
        handleError,
      }) =>
        loadEmployeeRecords({
          service: PayrollService.getPayrolls,
          mergeEmployees,

          transform: (records) =>
            records.map((payroll) => ({
              ...payroll,

              onPdf: async (id) => {
                try {
                  await downloadPayslip(id);

                  showAlert(
                    "success",
                    "Payslip downloaded successfully."
                  );
                } catch (error) {
                  handleError(
                    error,
                    "Failed to download payslip."
                  );
                }
              },
            })),
        })
      }
      filterData={(records, { location }) => {
        if (employeeId) {
          return records.filter(
            (payroll) =>
              Number(payroll.employee) ===
              Number(employeeId)
          );
        }

        if (location.pathname === "/me/payroll") {
          return records.filter(
            (payroll) =>
              Number(payroll.employee) ===
              Number(loggedEmployee?.id)
          );
        }

        return records;
      }}
      onButtonClick={({ navigate }) =>
        navigate("/payroll/create")
      }
      errorMessage="Failed to load payroll records."
    />
  );
};

export default Payroll;