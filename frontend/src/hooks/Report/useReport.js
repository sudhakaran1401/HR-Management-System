import { useEffect, useMemo, useState } from "react";

import useAlert from "../useAlert";
import useTable from "../useTable";
import useReportFilters from "./useReportFilters";

import loadEmployeeRecords from "../../utils/loadEmployeeRecords";
import { mergeEmployeeDetails } from "../../utils/mergeEmployeeDetails";
import { filterReportData } from "../../utils/filterReportData";

const useReport = ({
  service,
  dateField,
  hasEmployee = true,
  employeeField = "employee",
  transformRecords = null,
}) => {
  const { alert, showAlert, closeAlert } = useAlert();

  const [records, setRecords] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);

  const {
    month,
    year,
    employee,

    appliedMonth,
    appliedYear,
    appliedEmployee,

    reportGenerated,

    setMonth,
    setYear,
    setEmployee,

    handleGenerate,
    handleReset,
  } = useReportFilters(hasEmployee);

  useEffect(() => {
    loadData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);

      if (hasEmployee) {
        const {
          records: reportData,
          employees: employeeData,
        } = await loadEmployeeRecords({
          service,
          returnRaw: true,
        });

        setEmployees(employeeData);

        const merged = mergeEmployeeDetails(
          reportData,
          employeeData,
          employeeField
        );

        setRecords(
          transformRecords
            ? transformRecords(merged)
            : merged
        );
      } else {
        const reportData = await service();

        setRecords(
          transformRecords
            ? transformRecords(reportData)
            : reportData
        );
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const filteredRecords = useMemo(() => {
    return filterReportData({
      records,
      dateField,
      month: appliedMonth,
      year: appliedYear,
      employee: appliedEmployee,
      employeeField,
    });
  }, [
    records,
    dateField,
    appliedMonth,
    appliedYear,
    appliedEmployee,
    employeeField,
  ]);

  const table = useTable(filteredRecords);

  return {
    loading,

    alert,
    showAlert,
    closeAlert,

    employees,

    records,
    filteredRecords,

    table,

    month,
    year,
    employee,

    appliedMonth,
    appliedYear,
    appliedEmployee,

    reportGenerated,

    setMonth,
    setYear,
    setEmployee,

    handleGenerate,
    handleReset,

    reload: loadData,
  };
};

export default useReport;