import { useMemo } from "react";
import useChartTheme from "../../hooks/useChartTheme";

import {
  Chart as ChartJS,
  ArcElement,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
  Title,
  Filler,
} from "chart.js";

import { Pie, Bar, Line } from "react-chartjs-2";

ChartJS.register(
  ArcElement,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
  Title,
  Filler
);

function DashboardCharts({
  isEmployee = false,

  deptLabels = [],
  deptCounts = [],

  attendanceCounts = [],

  attendanceLabels = [],
  attendanceData = [],

  payrollLabels = [],
  payrollTotals = [],
}) {

  const { dark, textColor, gridColor, } = useChartTheme();

  const commonOptions = useMemo(
    () => ({
      responsive: true,
      maintainAspectRatio: false,

      plugins: {
        legend: {
          position: "top",
          labels: {
            color: textColor,
            boxWidth: 14,
            padding: 15,
          },
        },
      },

      scales: {
        x: {
          ticks: {
            color: textColor,
          },
          grid: {
            color: gridColor,
          },
        },

        y: {
          beginAtZero: true,

          ticks: {
            color: textColor,
          },

          grid: {
            color: gridColor,
          },
        },
      },
    }),
    [textColor, gridColor]
  );

  const pieOptions = useMemo(
    () => ({
      responsive: true,
      maintainAspectRatio: false,

      plugins: {
        legend: {
          position: "bottom",

          labels: {
            color: textColor,
            boxWidth: 15,
            padding: 15,
          },
        },
      },
    }),
    [textColor]
  );
  // ===============================
// EMPLOYEE DASHBOARD
// ===============================

if (isEmployee) {

  const employeeAttendanceChart = {
    labels: attendanceLabels,
    datasets: [
      {
        label: "Days Worked",
        data: attendanceData,
        borderColor: "#198754",
        backgroundColor: "rgba(25,135,84,0.15)",
        fill: true,
        tension: 0.4,
        pointRadius: 2,
        borderWidth: 3,
      },
    ],
  };

  const employeePayrollChart = {
    labels: payrollLabels,
    datasets: [
      {
        label: "Salary Received",
        data: payrollTotals,
        backgroundColor: "#0d6efd",
        borderRadius: 8,
      },
    ],
  };

  return (
    <div className="row g-4">

      {/* Worked Days */}

      <div className="col-md-6">

        <div className="card shadow-sm h-100">

          <div className="card-body">

            <h5 className="mb-3">
              Worked Days
            </h5>

            <div className="chart-container">

              <Line
                key={`attendance-${dark}`}
                data={employeeAttendanceChart}
                options={commonOptions}
              />

            </div>

          </div>

        </div>

      </div>

      {/* Payroll */}

      <div className="col-md-6">

        <div className="card shadow-sm h-100">

          <div className="card-body">

            <h5 className="mb-3">
              Payroll
            </h5>

            <div className="chart-container">

              <Bar
                key={`payroll-${dark}`}
                data={employeePayrollChart}
                options={commonOptions}
              />

            </div>

          </div>

        </div>

      </div>

    </div>
  );
}
// ===============================
// HR DASHBOARD
// ===============================

const departmentData = {
  labels: deptLabels,
  datasets: [
    {
      label: "Employees",
      data: deptCounts,
      backgroundColor: [
        "#0d6efd",
        "#198754",
        "#dc3545",
        "#ffc107",
        "#0dcaf0",
        "#6f42c1",
        "#fd7e14",
        "#20c997",
        "#e83e8c",
        "#6610f2",
      ],
      borderColor: "#ffffff",
      borderWidth: 2,
      hoverOffset: 10,
    },
  ],
};

const attendanceDataHR = {
  labels: ["Attendance"],
  datasets: [
    {
      label: "Present",
      data: [attendanceCounts?.[0] || 0],
      backgroundColor: "#198754",
    },
    {
      label: "Leave",
      data: [attendanceCounts?.[1] || 0],
      backgroundColor: "#dc3545",
    },
  ],
};

const payrollDataHR = {
  labels: payrollLabels,
  datasets: [
    {
      label: "Total Salary Paid",
      data: payrollTotals,
      borderColor: "#0d6efd",
      backgroundColor: "rgba(13,110,253,0.20)",
      fill: true,
      tension: 0.3,
      pointRadius: 4,
    },
  ],
};

return (
  <div className="row mt-4">

    {/* Department */}

    <div className="col-md-4">

      <div className="card shadow-sm h-100">

        <div className="card-body">

          <h5 className="mb-3">
            Employees by Department
          </h5>

          <div className="chart-container">

            <Pie
              key={`department-${dark}`}
              data={departmentData}
              options={pieOptions}
            />

          </div>

        </div>

      </div>

    </div>

    {/* Attendance */}

    <div className="col-md-4">

      <div className="card shadow-sm h-100">

        <div className="card-body">

          <h5 className="mb-3">
            Attendance
          </h5>

          <div className="chart-container">

            <Bar
              key={`attendance-hr-${dark}`}
              data={attendanceDataHR}
              options={commonOptions}
            />

          </div>

        </div>

      </div>

    </div>

    {/* Payroll */}

    <div className="col-md-4">

      <div className="card shadow-sm h-100">

        <div className="card-body">

          <h5 className="mb-3">
            Payroll Status
          </h5>

          <div className="chart-container">

            <Line
              key={`payroll-hr-${dark}`}
              data={payrollDataHR}
              options={commonOptions}
            />

          </div>

        </div>

      </div>

    </div>

  </div>
);
}
export default DashboardCharts;