const DetailCard = ({
  title,
  children,
  className = "",
  bodyClass = "",
}) => {
  return (
    <div className={`card shadow-sm ${className}`}>
      <div className={`card-body ${bodyClass}`}>
        {title && (
          <h4 className="mb-4">
            {title}
          </h4>
        )}

        {children}
      </div>
    </div>
  );
};

const EmployeeProfileCard = ({
  employee,
  actions = null,
}) => {
  if (!employee) return null;

  return (
    <div className="card shadow-sm">
      <div className="card-body text-center">

        {employee.photo ? (
          <img
            src={employee.photo}
            alt={employee.name}
            className="rounded-circle mb-3 profile-photo"
          />
        ) : (
          <div className="rounded-circle bg-primary text-white d-flex justify-content-center align-items-center mx-auto mb-3 profile-avatar">
            {employee.name?.charAt(0).toUpperCase()}
          </div>
        )}

        <h4>{employee.name}</h4>

        <div className="text-muted">
          {employee.designation}
        </div>

        <div className="text-muted mb-4">
          {employee.department}
        </div>

        <div className="d-grid gap-3">

          <a
            href={`mailto:${employee.email}`}
            className="btn btn-primary"
          >
            Email
          </a>

          <a
            href={`tel:${employee.phone}`}
            className="btn btn-outline-primary"
          >
            Call
          </a>

          {actions}

        </div>

      </div>
    </div>
  );
};

const LeaveSummaryCard = ({ balance }) => {
  if (!balance) return null;

  const rows = [
    {
      label: "Sick Leaves",
      applied: balance.sick_applied,
      max: balance.SICK_MAX,
      badge: "leave-badge-success",
    },
    {
      label: "Casual Leaves",
      applied: balance.casual_applied,
      max: balance.CASUAL_MAX,
      badge: "leave-badge-warning",
    },
    {
      label: "Annual Leaves",
      applied: balance.annual_applied,
      max: balance.ANNUAL_MAX,
      badge: "leave-badge-info",
    },
  ];

  return (
    <div className="card shadow-sm border-0 mb-4 leave-summary-card">
      <div className="card-body">

        <h4 className="fw-450 mb-4">
          Leave Taken Summary
        </h4>

        {rows.map((row) => (
          <div
            key={row.label}
            className="d-flex justify-content-between align-items-center py-3 leave-summary-row"
          >
            <span>{row.label}</span>

            <span className={`badge leave-badge ${row.badge}`}>
              {row.applied}/{row.max}
            </span>
          </div>
        ))}

        <div className="d-flex justify-content-between align-items-center pt-3">
          <strong>Total Leaves</strong>

          <span className="badge leave-badge leave-badge-danger">
            {balance.total_applied}/{balance.TOTAL_MAX}
          </span>
        </div>

      </div>
    </div>
  );
};

export {
  DetailCard,
  EmployeeProfileCard,
  LeaveSummaryCard,
};