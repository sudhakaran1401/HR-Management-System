import ViewButton from "../ViewButton";

/* ==========================================================
   COMMON CARD WRAPPER
========================================================== */

function DashboardCardBase({
  title,
  children,
  buttonText,
  onClick,
  center = false,
}) {
  return (
    <div className="col-md-3 mb-3">
      <div className="card shadow-sm h-100">
        <div
          className={`card-body ${
            center ? "text-center" : ""
          }`}
        >
          <h6 className="text-body-secondary">
            {title}
          </h6>

          {children}

          {buttonText && (
            <ViewButton
              text={buttonText}
              onClick={onClick}
            />
          )}
        </div>
      </div>
    </div>
  );
}

/* ==========================================================
   KPI CARD
========================================================== */

export function KPICard({
  title,
  value,
  color = "primary",
  subtitle,
  buttonText,
  onClick,
}) {
  return (
    <DashboardCardBase
      title={title}
      buttonText={buttonText}
      onClick={onClick}
      center={true}
    >
      {subtitle && (
        <h6 className={`text-${color}`}>
          {subtitle}
        </h6>
      )}

      <h3 className={`text-${color}`}>
        {value}
      </h3>
    </DashboardCardBase>
  );
}

/* ==========================================================
   ATTENDANCE CARD
========================================================== */

export function AttendanceCard({
  title,
  present,
  absent,
  buttonText,
  onClick,
}) {
  return (
    <DashboardCardBase
      title={title}
      buttonText={buttonText}
      onClick={onClick}
    >
      <div className="d-flex justify-content-between">
        <div>
          <h6 className="text-success">
            Present
          </h6>

          <h3 className="text-success">
            {present}
          </h3>
        </div>

        <div>
          <h6 className="text-danger">
            Leave
          </h6>

          <h3 className="text-danger">
            {absent}
          </h3>
        </div>
      </div>
    </DashboardCardBase>
  );
}

/* ==========================================================
   LEAVE CARD
========================================================== */

export function LeaveCard({
  title,
  pending,
  approved,
  rejected,
  buttonText,
  onClick,
}) {
  return (
    <DashboardCardBase
      title={title}
      buttonText={buttonText}
      onClick={onClick}
    >
      <div className="d-flex justify-content-between text-center">
        <div>
          <h6 className="text-warning">
            Pending
          </h6>

          <h3 className="text-warning">
            {pending}
          </h3>
        </div>

        <div>
          <h6 className="text-success">
            Approved
          </h6>

          <h3 className="text-success">
            {approved}
          </h3>
        </div>

        <div>
          <h6 className="text-danger">
            Rejected
          </h6>

          <h3 className="text-danger">
            {rejected}
          </h3>
        </div>
      </div>
    </DashboardCardBase>
  );
}