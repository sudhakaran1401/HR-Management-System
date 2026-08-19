import { useMemo } from "react";
import { useNavigate } from "react-router-dom";

import DashboardPage from "../../components/dashboard/DashboardPage";
import KPIGrid from "../../components/dashboard/KPIGrid";
import DashboardCharts from "../../components/dashboard/DashboardCharts";
import ReportButtons from "../../components/dashboard/ReportButtons";
import EmptyDashboardCard from "../../components/dashboard/EmptyDashboardCard";

import { KPICard, AttendanceCard, LeaveCard, } from "../../components/dashboard/DashboardCard";

import useDashboard from "../../hooks/useDashboard";

function HRDashboard() {
  const navigate = useNavigate();

  const INITIAL_DATA = {
    total_employees: 0,
    present_count: 0,
    absent_count: 0,
    pending_leaves: 0,
    approved_leaves: 0,
    rejected_leaves: 0,
    payroll_records_this_month: 0,
    dept_labels: [],
    dept_counts: [],
    attendance_counts: [],
    payroll_labels: [],
    payroll_totals: [],
  };

  const {
    alert,
    closeAlert,
    data,
    year,
    month,
    day,
    setYear,
    setMonth,
    setDay,
    dashboardMode,
    isHR,
    fetchDashboard,
    handleReset,
    handleRoleToggle,
  } = useDashboard({
    endpoint: "/api/dashboard/hr/",
    initialData: INITIAL_DATA,
  });

  const headerProps = {
    year,
    setYear,
    month,
    setMonth,
    day,
    setDay,
    onFilter: fetchDashboard,
    onReset: handleReset,
    dashboardMode,
    onToggleRole: handleRoleToggle,
    isHR,
  };

  const cards = useMemo(
    () => [
      {
        component: KPICard,
        props: {
          title: "Employees",
          value: data.total_employees,
          subtitle: "Total",
          color: "primary",
          buttonText: "View",
          onClick: () => navigate("/employees"),
        },
      },
      {
        component: AttendanceCard,
        props: {
          title: "Attendance",
          present: data.present_count,
          absent: data.absent_count,
          buttonText: "View",
          onClick: () => navigate("/attendance"),
        },
      },
      {
        component: LeaveCard,
        props: {
          title: "Leaves",
          pending: data.pending_leaves,
          approved: data.approved_leaves,
          rejected: data.rejected_leaves,
          buttonText: "View",
          onClick: () => navigate("/leaverequests"),
        },
      },
      {
        component: KPICard,
        props: {
          title: "Payroll",
          value: data.payroll_records_this_month,
          subtitle: "Total",
          color: "primary",
          buttonText: "View",
          onClick: () => navigate("/payroll"),
        },
      },
    ],
    [data, navigate]
  );

  const reportButtons = useMemo(
    () => [
      {
        label: "Employees Report",
        className: "btn btn-primary",
        path: "/employees-report",
      },
      {
        label: "Attendance Report",
        className: "btn btn-success",
        path: "/attendance-report",
      },
      {
        label: "Leave Report",
        className: "btn btn-warning text-white",
        path: "/leave-report",
      },
      {
        label: "Payroll Report",
        className: "btn btn-dark",
        path: "/payroll-report",
      },
    ],
    []
  );

  return (
    <DashboardPage
      title="HR Dashboard"
      alert={alert}
      onClose={closeAlert}
      headerProps={headerProps}
    >
      <KPIGrid cards={cards} />

      <div className="mt-4">
        {data.dept_labels?.length ? (
          <DashboardCharts
            deptLabels={data.dept_labels}
            deptCounts={data.dept_counts}
            attendanceCounts={data.attendance_counts}
            payrollLabels={data.payroll_labels}
            payrollTotals={data.payroll_totals}
          />
        ) : (
          <EmptyDashboardCard />
        )}
      </div>

      <ReportButtons buttons={reportButtons} />
    </DashboardPage>
  );
}

export default HRDashboard;