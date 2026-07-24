import StatusBadge from "../../components/StatusBadge";
import { formatDate, formatTime, } from "../../utils/formatters";

export const attendanceColumns = [
  {
    key: "employee",
    title: "Employee",
    width: "220px",
    render: (row) => row.employeeDetails?.name || "-",
  },

  {
    key: "department",
    title: "Department",
    width: "170px",
    render: (row) => row.employeeDetails?.department || "-",
  },

  {
    key: "date",
    title: "Date",
    width: "150px",
    render: (row) => formatDate(row.date),
  },

  {
    key: "status",
    title: "Status",
    width: "130px",
    render: (row) => (
      <StatusBadge
        status={row.status}
        fallback="Not marked"
      />
    ),
  },

  {
    key: "check_in",
    title: "Check In",
    width: "130px",
    render: (row) => formatTime(row.check_in),
  },

  {
    key: "check_out",
    title: "Check Out",
    width: "130px",
    render: (row) => formatTime(row.check_out),
  },

  {
    key: "remarks",
    title: "Remarks",
    render: (row) => row.remarks || "-",
  },
];