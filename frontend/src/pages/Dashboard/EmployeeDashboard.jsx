import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import DashboardPage from "../../components/dashboard/DashboardPage";
import KPIGrid from "../../components/dashboard/KPIGrid";
import ProfileCard from "../../components/dashboard/ProfileCard";
import DashboardCharts from "../../components/dashboard/DashboardCharts";
import EmptyDashboardCard from "../../components/dashboard/EmptyDashboardCard";
import { KPICard } from "../../components/dashboard/DashboardCard";
import api from "../../services/api";
import useDashboard from "../../hooks/useDashboard";

function EmployeeDashboard() {
  const navigate = useNavigate();

  const INITIAL_DATA = {
    my_attendance_month: 0,
    leave_balance: 0,
    salary_count: 0,
    latest_salary: null,
    attendance_month_labels: [],
    attendance_month_data: [],
    payroll_month_labels: [],
    payroll_month_data: [],
  };

  const [profile, setProfile] = useState(null);

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
    endpoint: "/api/dashboard/employee/",
    initialData: INITIAL_DATA,
  });

  useEffect(() => {
    const loadProfile = async () => {
      try {
        const { data: user } = await api.get("/api/me/");
        const { data: employee } = await api.get(
          `/api/employees/${user.id}/`
        );

        setProfile(employee);
      } catch (err) {
        console.error(err);
      }
    };

    loadProfile();
  }, []);

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
          title: "Worked Days",
          value: data.my_attendance_month,
          color: "success",
          buttonText: "View",
          onClick: () => navigate("/me/attendance-status"),
        },
      },
      {
        component: KPICard,
        props: {
          title: "Leave Balance",
          value: data.leave_balance,
          color: "warning",
          buttonText: "View",
          onClick: () => navigate("/leave-balance"),
        },
      },
      {
        component: KPICard,
        props: {
          title: "Latest Salary",
          value: `₹${data.latest_salary?.net_pay || 0}`,
          color: "primary",
          buttonText: "View",
          onClick: () => navigate("/me/payroll"),
        },
      },
      {
        component: KPICard,
        props: {
          title: "Payroll Count",
          value: data.salary_count,
          color: "dark",
          buttonText: "View",
          onClick: () => navigate("/me/payroll"),
        },
      },
    ],
    [data, navigate]
  );

  return (
    <DashboardPage
      title="Employee Dashboard"
      alert={alert}
      onClose={closeAlert}
      headerProps={headerProps}
    >
      <KPIGrid cards={cards} />

      <div className="row mt-4">
        <div className="col-md-4">
          <ProfileCard profile={profile} />
        </div>

        <div className="col-md-8">
          {data.attendance_month_labels?.length ? (
            <DashboardCharts
              isEmployee
              attendanceLabels={data.attendance_month_labels}
              attendanceData={data.attendance_month_data}
              payrollLabels={data.payroll_month_labels}
              payrollTotals={data.payroll_month_data}
            />
          ) : (
            <EmptyDashboardCard fullHeight />
          )}
        </div>
      </div>
    </DashboardPage>
  );
}

export default EmployeeDashboard;