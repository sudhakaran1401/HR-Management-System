import { useEffect, useMemo, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import Loader from "../../components/Loader";
import PageHeader from "../../components/PageHeader";
import ActionButtons from "../../components/ActionButtons";

import { DetailTable } from "../../components/detail/DetailTable";
import { EmployeeProfileCard } from "../../components/detail/DetailCard";

import api from "../../services/api";

const EmployeeView = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  const isHRView = Boolean(id);

  const [employee, setEmployee] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchEmployee();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  const fetchEmployee = async () => {
    try {
      const { data } = await api.get(
        id
          ? `/api/employees/${id}/`
          : "/api/employees/me/"
      );

      setEmployee(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const actions = useMemo(() => {
    if (isHRView) {
      return [
        {
          label: "Edit",
          className: "btn btn-warning text-white",
          path: `/employees/edit/${id}`,
        },
        {
          label: "Delete",
          className: "btn btn-danger",
          path: `/employees/delete/${id}`,
        },
        {
          label: "Attendance",
          className: "btn btn-primary",
          path: `/employee/${id}/mark-attendance`,
        },
        {
          label: "Leaves",
          className: "btn btn-outline-light",
          path: `/employee/${id}/leave-balance`,
        },
        {
          label: "Salary",
          className: "btn btn-success",
          path: `/employee/${id}/payroll`,
        },
      ];
    }

    return [
      {
        label: "Attendance",
        className: "btn btn-primary",
        path: "/me/attendance",
      },
      {
        label: "Leaves",
        className: "btn btn-outline-light",
        path: "/leave-balance",
      },
      {
        label: "Salary",
        className: "btn btn-success",
        path: "/me/payroll",
      },
    ];
  }, [id, isHRView]);

  const details = useMemo(() => {
    if (!employee) return [];

    return [
      ["Employee ID", `#${employee.id}`],
      ["Name", employee.name],
      ["Email", employee.email],
      ["Phone", employee.phone],
      ["Department", employee.department],
      ["Designation", employee.designation],
      [
        "Joining Date",
        employee.joining_date
          ? new Date(employee.joining_date).toLocaleDateString(
              "en-US",
              {
                year: "numeric",
                month: "long",
                day: "numeric",
              }
            )
          : "-",
      ],
      ["Date of Birth", employee.dob || "-"],
      ["Address", employee.address || "-"],
    ];
  }, [employee]);

  if (loading) {
    return (
      <Loader title="Loading Employee..." />
    );
  }

  if (!employee) {
    return (
      <div className="container py-5 text-center">
        <h3>Employee not found</h3>
      </div>
    );
  }

  return (
    <div className="container py-4">

      <PageHeader
        title="Profile"
        actions={
          <ActionButtons>
            {actions.map((action) => (
              <button
                key={action.label}
                className={action.className}
                onClick={() => navigate(action.path)}
              >
                {action.label}
              </button>
            ))}
          </ActionButtons>
        }
      />

      <div className="row g-4">

        <div className="col-lg-4">
          <EmployeeProfileCard
            employee={employee}
          />
        </div>

        <div className="col-lg-8">

          <div className="card shadow-sm">
            <div className="card-body">

              <h4 className="mb-4">
                Employee Details
              </h4>

              <DetailTable
                details={details}
              />

            </div>
          </div>

        </div>

      </div>

    </div>
  );
};

export default EmployeeView;