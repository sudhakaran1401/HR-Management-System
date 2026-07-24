import AlertMessage from "../AlertMessage";
import EmptyReport from "./EmptyReport";
import ReportLayout from "../../layouts/ReportLayout";

import useReport from "../../hooks/Report/useReport";
import useReportExport from "../../hooks/Report/useReportExport";

import { REPORT_YEARS } from "../../config/constants/reportYears";

const BaseReport = ({
  title,

  service,
  dateField,

  hasEmployee = true,
  employeeField = "employee",

  transformRecords,

  columns,

  csvAction,
  pdfAction,
  moduleName,

  buildReport,
}) => {
  const {
    loading,

    alert,
    showAlert,
    closeAlert,

    employees,

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
  } = useReport({
    service,
    dateField,
    hasEmployee,
    employeeField,
    transformRecords,
  });

  // Build report only once
  const {
    chartTitle,
    chart,
    summaryCards = [],
  } = buildReport(filteredRecords);

  const exportParams = {
    year: appliedYear,
    month: appliedMonth,
  };

  if (hasEmployee) {
    exportParams.employee = appliedEmployee;
  }

  const { handleCSV, handlePDF } = useReportExport({
    showAlert,
    csvAction,
    pdfAction,
    moduleName,
    params: exportParams,
  });

  return (
    <>
      <AlertMessage
        show={alert.show}
        type={alert.type}
        message={alert.message}
        onClose={closeAlert}
      />

      <ReportLayout
        title={title}
        reportGenerated={reportGenerated}
        month={month}
        year={year}
        employee={employee}
        years={REPORT_YEARS}
        employees={employees}
        showEmployee={hasEmployee}
        hasSummary={summaryCards.length > 0}
        summaryCards={summaryCards}
        chartTitle={chartTitle}
        chart={chart}
        columns={columns}
        data={table.paginatedData}
        loading={loading}
        table={table}
        onMonthChange={setMonth}
        onYearChange={setYear}
        onEmployeeChange={setEmployee}
        onGenerate={handleGenerate}
        onReset={handleReset}
        onExportCSV={handleCSV}
        onExportPDF={handlePDF}
      >
        <EmptyReport />
      </ReportLayout>
    </>
  );
};

export default BaseReport;