const DetailTable = ({
  details = [],
  labelWidth = "220",
  tableClass = "table",
}) => {
  return (
    <table className={tableClass}>
      <tbody>
        {details.map(([label, value]) => (
          <tr key={label}>
            <th width={labelWidth}>
              {label}
            </th>

            <td>{value}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

const formatCurrency = (value) =>
  `₹${Number(value || 0).toLocaleString()}`;

const SalaryTable = ({ salary }) => {
  if (!salary) return null;

  return (
    <div className="table-responsive">
      <table className="table table-bordered align-middle">
        <thead className="table-light text-center">
          <tr>
            <th>Earnings</th>
            <th>Amount</th>
            <th>Deductions</th>
            <th>Amount</th>
          </tr>
        </thead>

        <tbody>
          <tr>
            <td>Basic</td>
            <td>{formatCurrency(salary.basic)}</td>

            <td>PF</td>
            <td>{formatCurrency(salary.pf)}</td>
          </tr>

          <tr>
            <td>HRA</td>
            <td>{formatCurrency(salary.hra)}</td>

            <td>Tax</td>
            <td>{formatCurrency(salary.tax)}</td>
          </tr>

          <tr>
            <td>Allowances</td>
            <td>{formatCurrency(salary.allowances)}</td>

            <td>Other</td>
            <td>{formatCurrency(salary.other_deductions)}</td>
          </tr>

          <tr className="table-secondary fw-bold">
            <td>Gross</td>
            <td>{formatCurrency(salary.stored_gross)}</td>

            <td>Total Deductions</td>
            <td>
              {formatCurrency(
                salary.stored_total_deductions
              )}
            </td>
          </tr>

          <tr>
            <td colSpan={2}></td>

            <td className="fw-bold">
              Net Pay
            </td>

            <td className="fw-bold text-success">
              {formatCurrency(salary.stored_net_pay)}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export {
  DetailTable,
  SalaryTable,
};