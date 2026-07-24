function DashboardHeader({
  title,
  year,
  setYear,
  month,
  setMonth,
  day,
  setDay,
  onFilter,
  onReset,
  dashboardMode,
  onToggleRole,
  isHR,
}) {
  const years = ["Year", "2025", "2026", "2027", "2028", "2029", "2030"];

  const months = [
    { value: "", label: "Month" },
    { value: "1", label: "January" },
    { value: "2", label: "February" },
    { value: "3", label: "March" },
    { value: "4", label: "April" },
    { value: "5", label: "May" },
    { value: "6", label: "June" },
    { value: "7", label: "July" },
    { value: "8", label: "August" },
    { value: "9", label: "September" },
    { value: "10", label: "October" },
    { value: "11", label: "November" },
    { value: "12", label: "December" },
  ];

  return (
    <div className="dashboard-header d-flex justify-content-between align-items-center mb-4 px-4 py-3">
      <h3 className="mb-0 fw-bold">{title}</h3>

      <div className="d-flex gap-3 align-items-center">

        {/* Show Toggle Only For HR */}
        {isHR && (
          <div className="d-flex align-items-center gap-2">

            <span
              className={`fw-semibold ${
                dashboardMode === "hr"
                  ? ""
                  : "text-light opacity-75"
              }`}
            >
              HR
            </span>

            <div className="form-check form-switch m-0">
              <input
                className="form-check-input"
                type="checkbox"
                checked={dashboardMode === "employee"}
                onChange={onToggleRole}
              />
            </div>

            <span
              className={`fw-semibold ${
                dashboardMode === "employee"
                  ? ""
                  : "text-light opacity-75"
              }`}
            >
              Employee
            </span>

          </div>
        )}

        {/* Year */}
        <select
          className="form-select form-select-sm"
          value={year}
          onChange={(e) => setYear(e.target.value)}
        >
          {years.map((y) => (
            <option key={y} value={y}>
              {y}
            </option>
          ))}
        </select>

        {/* Month */}
        <select
          className="form-select form-select-sm"
          value={month}
          onChange={(e) => setMonth(e.target.value)}
        >
          {months.map((m) => (
            <option key={m.value} value={m.value}>
              {m.label}
            </option>
          ))}
        </select>

        {/* Day */}
        <select
          className="form-select form-select-sm"
          value={day}
          onChange={(e) => setDay(e.target.value)}
        >
          <option value="">Day</option>

          {[...Array(31)].map((_, index) => (
            <option key={index + 1} value={index + 1}>
              {index + 1}
            </option>
          ))}
        </select>

        <button
          className="btn btn-primary btn-sm"
          onClick={onFilter}
        >
          Filter
        </button>

        <button
          className="btn btn-dark btn-sm"
          onClick={onReset}
        >
          Reset
        </button>

      </div>
    </div>
  );
}

export default DashboardHeader;