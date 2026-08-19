
  // ====== DEPARTMENT CHART ======
  const deptLabels = JSON.parse(
    document.getElementById('dept-labels').textContent
  );

  const deptData = JSON.parse(
    document.getElementById('dept-counts').textContent
  );

  const deptCtx = document.getElementById('deptChart').getContext('2d');

  new Chart(deptCtx, {
  type: 'pie', 
  data: {
    labels: deptLabels,
    datasets: [{
      label: 'Employees',
      data: deptData,
      backgroundColor: [
        '#0d6efd', 
        '#198754', 
        '#dc3545', 
        '#ffc107', 
        '#0dcaf0', 
        '#6f42c1', 
        '#fd7e14', 
        '#20c997', 
        '#e83e8c', 
        '#6610f2'  
      ],
      borderColor: '#ffffff',
      borderWidth: 2
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'left'
      }
    }
  }
});


  // ====== ATTENDANCE CHART ======
  const attLabels = JSON.parse(
    document.getElementById('attendance-labels').textContent
  );

  const attData = JSON.parse(
    document.getElementById('attendance-counts').textContent
  );

  const attCtx = document.getElementById('attendanceChart').getContext('2d');

  new Chart(attCtx, {
  type: 'bar',
  data: {
    labels: ['Attendance'],  // single category
    datasets: [
      {
        label: 'Present',
        data: [attData[0]],
        backgroundColor: '#28a745'
      },
      {
        label: 'Absent',
        data: [attData[1]],
        backgroundColor: '#dc3545'
      }
    ]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,

    plugins: {
      legend: {
        display: true,
        labels: {
          color: "#e5e7eb",
          font: {
            size: 13,
            weight: "bold"
          }
        }
      }
    },

    scales: {
      x: {
        ticks: { color: "#e5e7eb" },
        grid: { color: "rgba(255,255,255,0.05)" }
      },
      y: {
        ticks: { color: "#e5e7eb" },
        grid: { color: "rgba(255,255,255,0.05)" }
      }
    }
  }
});

  // ====== PAYROLL CHART ======
  const payrollLabels = JSON.parse(
    document.getElementById('payroll-labels').textContent
  );

  const payrollTotals = JSON.parse(
    document.getElementById('payroll-totals').textContent
  );

  const payrollCtx = document.getElementById('payrollChart').getContext('2d');

  new Chart(payrollCtx, {
    type: 'line',
    data: {
      labels: payrollLabels,
      datasets: [{
        label: 'Total Salary Paid',
        data: payrollTotals,
        borderColor: '#0d6efd',
        backgroundColor: 'rgba(13,110,253,0.2)',
        fill: true,
        tension: 0.3,
        pointRadius: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
