import { useMemo } from "react";
import useChartTheme from "../../hooks/useChartTheme";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Tooltip,
  Legend,
} from "chart.js";

import { Bar, Pie, Line, Doughnut, } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Tooltip,
  Legend
);

function ReportChart({
  title,
  type = "bar",
  chartData,
  options = {},
}) {

  const { dark, textColor, gridColor, } = useChartTheme();

  const defaultOptions = useMemo(() => ({

    responsive: true,
    maintainAspectRatio: false,

    plugins: {
      legend: {
        labels: {
          color: textColor,
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

  }), [textColor, gridColor]);

  const chartOptions = useMemo(() => ({

    ...defaultOptions,
    ...options,

    plugins: {

      ...defaultOptions.plugins,
      ...options.plugins,

      legend: {

        ...defaultOptions.plugins.legend,
        ...options.plugins?.legend,

        labels: {

          ...defaultOptions.plugins.legend.labels,
          ...options.plugins?.legend?.labels,

          color: textColor,

        },

      },

    },

    scales: {

      ...defaultOptions.scales,
      ...options.scales,

      x: {

        ...defaultOptions.scales.x,
        ...options.scales?.x,

        ticks: {

          ...defaultOptions.scales.x.ticks,
          ...options.scales?.x?.ticks,

          color: textColor,

        },

        grid: {

          ...defaultOptions.scales.x.grid,
          ...options.scales?.x?.grid,

          color: gridColor,

        },

      },

      y: {

        ...defaultOptions.scales.y,
        ...options.scales?.y,

        ticks: {

          ...defaultOptions.scales.y.ticks,
          ...options.scales?.y?.ticks,

          color: textColor,

        },

        grid: {

          ...defaultOptions.scales.y.grid,
          ...options.scales?.y?.grid,

          color: gridColor,

        },

      },

    },

  }), [
    defaultOptions,
    options,
    textColor,
    gridColor,
  ]);

  const charts = {
    bar: Bar,
    line: Line,
    pie: Pie,
    doughnut: Doughnut,
  };

  const ChartComponent = charts[type];

  return (

    <div className="card shadow-sm border-0 w-100 h-100 report-chart-card">

      <div className="card-header fw-bold">
        {title}
      </div>

      <div className="card-body report-chart-body">

        <ChartComponent
          key={`${type}-${dark}`}
          data={chartData}
          options={chartOptions}
        />

      </div>

    </div>

  );

}

export default ReportChart;