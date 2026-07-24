import React from "react";
import ExportButtons from "./ExportButtons";

const ReportToolbar = ({
  month = "",
  year = "",
  employee = "",

  years = [],
  employees = [],

  showEmployee = true,

  onMonthChange,
  onYearChange,
  onEmployeeChange,

  onGenerate,
  onReset,
  onExportCSV,
  onExportPDF,
}) => {
  const months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];

  return (
    <div className="row g-3 align-items-end">

      {/* Month */}

      <div className="col-md-2">
        <label className="form-label">
          Month
        </label>

        <select
          className="form-select"
          value={month}
          onChange={(e) => onMonthChange(e.target.value)}
        >
          <option value="">---------</option>

          {months.map((m, index) => (
            <option
              key={index}
              value={index + 1}
            >
              {m}
            </option>
          ))}
        </select>
      </div>

      {/* Year */}

      <div className="col-md-2">
        <label className="form-label">
          Year
        </label>

        <select
          className="form-select"
          value={year}
          onChange={(e) => onYearChange(e.target.value)}
        >
          <option value="">------</option>

          {years.map((y) => (
            <option
              key={y}
              value={y}
            >
              {y}
            </option>
          ))}
        </select>
      </div>

      {/* Employee */}

      {showEmployee && (
        <div className="col-md-4">
          <label className="form-label">
            Employee
          </label>

          <select
            className="form-select"
            value={employee}
            onChange={(e) => onEmployeeChange(e.target.value)}
          >
            <option value="">---------</option>

            {employees.map((emp) => (
              <option
                key={emp.id}
                value={emp.id}
              >
                {emp.name}
              </option>
            ))}
          </select>
        </div>
      )}

      {/* Buttons */}

      <div className={showEmployee ? "col-md-4" : "col-md-8"}>

        <div className="d-flex flex-wrap gap-2">

          <button
            className="btn btn-primary btn-modern"
            onClick={onGenerate}
          >
            Generate
          </button>

          <button
            className="btn btn-secondary btn-modern text-white"
            onClick={onReset}
          >
            Reset
          </button>

          <ExportButtons
            onCSV={onExportCSV}
            onPDF={onExportPDF}
          />

        </div>

      </div>

    </div>
  );
};

export default ReportToolbar;