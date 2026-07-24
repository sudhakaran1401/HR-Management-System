import { useNavigate } from "react-router-dom";
import StatusBadge from "../../components/StatusBadge";
import { formatDate, formatDateTime, } from "../../utils/formatters";

export const leaveColumns = ({
  isHRPage,
  isMyLeavePage,
}) => {
  const navigate = useNavigate();

  return [
    {
      key: "employee",
      title: "Employee",
      width: "150px",
      render: (row) => row.employeeDetails?.name || "-",
    },

    {
      key: "department",
      title: "Department",
      width: "120px",
      render: (row) => row.employeeDetails?.department || "-",
    },

    {
      key: "leave_type",
      title: "Leave Type",
      width: "120px",
      render: (row) => row.leave_type,
    },

    {
      key: "days",
      title: "Days",
      width: "60px",
      render: (row) => row.days,
    },

    {
      key: "dates",
      title: "Dates",
      width: "260px",
      render: (row) =>
        `${formatDate(row.start_date)} - ${formatDate(row.end_date)}`,
    },

    {
      key: "reason",
      title: "Reason",
      render: (row) =>
        row.reason && row.reason !== "nan"
          ? row.reason
          : "-",
    },

    {
      key: "applied_at",
      title: "Applied",
      width: "230px",
      render: (row) =>
        formatDateTime(row.applied_at),
    },

    {
      key: "status",
      title: "Status",
      width: "110px",
      render: (row) => (
        <StatusBadge status={row.status} />
      ),
    },

    {
      key: "actions",
      title: "Actions",
      width: "180px",

      render: (row) => {
        if (row.status !== "PENDING") {
          return (
            <span className="text-muted">
              -
            </span>
          );
        }

        if (isHRPage) {
          return (
            <div className="d-flex gap-2">
              <button
                className="btn btn-success btn-sm"
                onClick={() =>
                  row.onApprove(row.id)
                }
              >
                Approve
              </button>

              <button
                className="btn btn-danger btn-sm"
                onClick={() =>
                  row.onReject(row.id)
                }
              >
                Reject
              </button>
            </div>
          );
        }

        if (isMyLeavePage) {
          return (
            <button
              className="btn btn-warning btn-sm"
              onClick={() =>
                navigate(
                  `/leaverequest/edit/${row.id}`
                )
              }
            >
              Update
            </button>
          );
        }

        return (
          <span className="text-muted">
            -
          </span>
        );
      },
    },
  ];
};