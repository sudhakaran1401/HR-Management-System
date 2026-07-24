import { Link } from "react-router-dom";

import {
  formatDate,
  formatMonth,
} from "../../utils/formatters";

export const payrollColumns = (isMyPayroll = false) => [
  {
    key: "employee",
    title: "Employee",
    width: "180px",
    render: (row) => row.employeeDetails?.name || "-",
  },

  {
    key: "designation",
    title: "Designation",
    width: "180px",
    render: (row) => row.employeeDetails?.designation || "-",
  },

  {
    key: "pay_month",
    title: "Month",
    width: "140px",
    render: (row) => formatMonth(row.pay_month),
  },

  {
    key: "gross",
    title: "Gross",
    width: "120px",
    render: (row) =>
      `₹${Number(row.stored_gross).toLocaleString()}`,
  },

  {
    key: "deductions",
    title: "Deductions",
    width: "140px",
    render: (row) =>
      `₹${Number(
        row.stored_total_deductions
      ).toLocaleString()}`,
  },

  {
    key: "net_pay",
    title: "Net Pay",
    width: "120px",
    render: (row) =>
      `₹${Number(
        row.stored_net_pay
      ).toLocaleString()}`,
  },

  {
    key: "paid_date",
    title: "Paid Date",
    width: "160px",
    render: (row) => formatDate(row.paid_date),
  },

  {
    key: "payslip",
    title: "Payslip",
    width: "170px",

    render: (row) => {
      const url = isMyPayroll
        ? `/me/payslip/${row.id}`
        : `/payroll/payslip/${row.id}`;

      return (
        <div className="d-flex gap-2">
          <Link
            to={url}
            className="btn btn-outline-primary btn-sm"
          >
            View
          </Link>

          <button
            className="btn btn-outline-secondary btn-sm"
            onClick={() => row.onPdf?.(row.id)}
          >
            PDF
          </button>
        </div>
      );
    },
  },
];