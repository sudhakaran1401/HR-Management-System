import { useEffect, useMemo, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import Loader from "../../components/Loader";
import PageHeader from "../../components/PageHeader";
import SummaryCards from "../../components/report/SummaryCards";

import { LeaveSummaryCard } from "../../components/detail/DetailCard";
import { getLeaveBalance } from "../../services/LeaveRequestService";

const LeaveBalance = () => {
  const navigate = useNavigate();
  const { employeeId } = useParams();

  const [balance, setBalance] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loggedEmployee = JSON.parse(
    localStorage.getItem("employee")
  );

  useEffect(() => {
    const fetchBalance = async () => {
      try {
        const data = await getLeaveBalance(employeeId);
        setBalance(data);
      } catch (error) {
        console.error(error);
        setError("Unable to load leave balance.");
      } finally {
        setLoading(false);
      }
    };

    fetchBalance();
  }, [employeeId]);

  const summaryCards = useMemo(() => {
    if (!balance) return [];

    return [
      {
        title: "Total Applied",
        value: balance.total,
        color: "#0d6efd",
      },
      {
        title: "Approved",
        value: balance.approved,
        color: "#198754",
      },
      {
        title: "Pending",
        value: balance.pending,
        color: "#ffc107",
      },
      {
        title: "Rejected",
        value: balance.rejected,
        color: "#dc3545",
      },
    ];
  }, [balance]);

  if (loading) {
    return <Loader />;
  }

  if (error) {
    return (
      <div className="alert alert-danger mt-4">
        {error}
      </div>
    );
  }

  return (
    <div className="container mt-4">

      <PageHeader title="Leave Balance" />

      <div className="mb-4">
        <span className="text-secondary">
          Employee :
        </span>

        <strong className="ms-2">
          {balance.employee}
        </strong>
      </div>

      <div className="mb-4">
        <SummaryCards
          cards={summaryCards}
          twoColumns={false}
        />
      </div>

      <LeaveSummaryCard
        balance={balance}
      />

      <div className="d-flex gap-3">

        {location.pathname === "/leave-balance" && (
          <button
            className="btn btn-primary leave-action-btn"
            onClick={() => navigate("/leaverequest/create")}
          >
            Apply Leave
          </button>
        )}

        <button
          className="btn btn-outline-primary leave-action-btn"
          onClick={() => {
            if (
              loggedEmployee?.department === "HR"
            ) {
              navigate(
                employeeId
                  ? `/employee/${employeeId}/leaverequests`
                  : "/me/leaverequests"
              );
            } else {
              navigate("/me/leaverequests");
            }
          }}
        >
          {loggedEmployee?.department === "HR" &&
          employeeId
            ? "Requests"
            : "My Requests"}
        </button>

      </div>

    </div>
  );
};

export default LeaveBalance;