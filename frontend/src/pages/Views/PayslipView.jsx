import { useEffect, useState } from "react";
import { useLocation, useNavigate, useParams, } from "react-router-dom";

import api from "../../services/api";
import { downloadPayslip } from "../../services/PayrollService";
import { DetailCard } from "../../components/detail/DetailCard";
import Loader from "../../components/Loader";
import PageHeader from "../../components/PageHeader";
import { SalaryTable } from "../../components/detail/DetailTable";

const PayslipView = () => {
  const { id } = useParams();

  const location = useLocation();
  const navigate = useNavigate();

  const isMyPayslip =
    location.pathname.startsWith("/me/payslip");

  const [salary, setSalary] = useState(null);
  const [employee, setEmployee] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchPayslip();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const fetchPayslip = async () => {
    try {
      const salaryRes = await api.get(`/api/payroll/${id}/`);
      setSalary(salaryRes.data);

      const employeeRes = await api.get(
        `/api/employees/${salaryRes.data.employee}/`
      );

      setEmployee(employeeRes.data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async () => {
    try {
      await downloadPayslip(id);
    } catch (error) {
      console.error(error);
    }
  };

  if (loading || !salary || !employee) {
    return (
      <Loader title="Loading Payslip..." />
    );
  }

  return (
    <div className="container py-4 payslip-page">

      <PageHeader
        title="Payslip Preview"
        actions={
          <>
            <button
              className="btn btn-light"
              onClick={handleDownload}
            >
              Download PDF
            </button>

            {!isMyPayslip && (
              <button
                className="btn btn-warning"
                onClick={() =>
                  navigate(`/payroll/edit/${id}`)
                }
              >
                Update
              </button>
            )}
          </>
        }
      />

      <div className="card shadow-sm payslip-card">

        <div className="card-body p-4">

          <h3 className="fw-bold mb-3">
            {employee.name}
          </h3>

          <p>
            <strong>Email:</strong>{" "}
            {employee.email}
          </p>

          <p>
            <strong>Department:</strong>{" "}
            {employee.department}
          </p>

          <p>
            <strong>Designation:</strong>{" "}
            {employee.designation}
          </p>

          <p>
            <strong>Pay Month:</strong>{" "}
            {new Date(
              salary.pay_month
            ).toLocaleDateString("en-US", {
              month: "short",
              year: "numeric",
            })}
          </p>

          <hr className="my-4" />

          <SalaryTable salary={salary} />

          {salary.notes && (
            <div className="alert alert-light mt-4">
              <strong>Notes:</strong>{" "}
              {salary.notes}
            </div>
          )}

        </div>

      </div>

    </div>
  );
};

export default PayslipView;