import LayoutHeader from "../components/LayoutHeader";

import ReportToolbar from "../components/report/ReportToolbar";
import SummaryCards from "../components/report/SummaryCards";
import ReportChart from "../components/report/ReportChart";

import DataTable from "../components/list/DataTable";
import TablePagination from "../components/list/TablePagination";

const ReportLayout = ({
  title,

  reportGenerated,

  month,
  year,
  employee,

  years = [],
  employees = [],
  showEmployee = true,

  hasSummary = false,
  summaryCards = [],

  chartTitle,
  chart,

  columns = [],
  data = [],
  loading = false,

  table,

  onMonthChange,
  onYearChange,
  onEmployeeChange,

  onGenerate,
  onReset,

  onExportCSV,
  onExportPDF,

  children,
}) => {
  return (
    <div className="container mt-4">
      <LayoutHeader title={title} />

      <div className="card shadow-sm border-0 mb-4">
        <div className="card-body">
          <ReportToolbar
            month={month}
            year={year}
            employee={employee}
            years={years}
            employees={employees}
            showEmployee={showEmployee}
            onMonthChange={onMonthChange}
            onYearChange={onYearChange}
            onEmployeeChange={onEmployeeChange}
            onGenerate={onGenerate}
            onReset={onReset}
            onExportCSV={onExportCSV}
            onExportPDF={onExportPDF}
          />
        </div>
      </div>

      {!reportGenerated ? (
        children
      ) : (
        <>
          {(hasSummary || chart) && (
            <div className="row g-4 mb-4">

              {hasSummary && summaryCards.length > 0 && (
                <div className="col-lg-4">
                  <SummaryCards cards={summaryCards} />
                </div>
              )}

              {chart && (
                <div
                  className={
                    hasSummary
                      ? "col-lg-8"
                      : "col-12"
                  }
                >
                  <ReportChart
                    title={chartTitle}
                    type={chart.type}
                    chartData={chart.data}
                    options={chart.options}
                  />
                </div>
              )}

            </div>
          )}

          <div className="card shadow-sm border-0">
            <div className="card-body">
              <DataTable
                columns={columns}
                data={data}
                loading={loading}
              />

              <TablePagination table={table} />
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default ReportLayout;