const STATUS_CONFIG = {
  Present: {
    label: "Present",
    className: "bg-success",
  },

  Leave: {
    label: "Leave",
    className: "bg-danger",
  },

  APPROVED: {
    label: "Approved",
    className: "bg-success",
  },

  REJECTED: {
    label: "Rejected",
    className: "bg-danger",
  },

  PENDING: {
    label: "Pending",
    className: "bg-warning text-dark",
  },
};

const StatusBadge = ({
  status,
  fallback = "Not marked",
}) => {
  if (!status) {
    return (
      <span className="badge bg-warning text-dark">
        {fallback}
      </span>
    );
  }

  const config = STATUS_CONFIG[status];

  if (!config) {
    return (
      <span className="badge bg-secondary">
        {status}
      </span>
    );
  }

  return (
    <span className={`badge ${config.className}`}>
      {config.label}
    </span>
  );
};

export default StatusBadge;