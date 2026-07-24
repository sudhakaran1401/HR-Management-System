
 const monthLabels = JSON.parse(
  document.getElementById("attendance-month-labels").textContent
);

const monthData = JSON.parse(
  document.getElementById("attendance-month-data").textContent
);

new Chart(
  document.getElementById("attendanceChart"),
  {
    type: "line",
    data: {
      labels: monthLabels,
      datasets: [{
        label: "Days Worked",
        data: monthData,
        borderColor: "#198754",
        backgroundColor: "rgba(25,135,84,0.2)",
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
          beginAtZero: true,
          min: 0,        
          max: 30,      
          ticks: {
            stepSize: 5  
          },
          title: {
            display: true,
            text: "Days Worked"
          }
        },
        x: {
          title: {
            display: true,
            text: "Month"
          }
        }
      }
    }
  }
);

const payrollLabels = JSON.parse(
  document.getElementById("payroll-month-labels").textContent
);

const payrollData = JSON.parse(
  document.getElementById("payroll-month-data").textContent
);

new Chart(
  document.getElementById("payrollChart"),
  {
    type: "bar",  
    data: {
      labels: payrollLabels,
      datasets: [{
        label: "Salary Received",
        data: payrollData,
        backgroundColor: "#0d6efd"
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: "Salary Amount"
          }
        },
        x: {
          title: {
            display: true,
            text: "Month"
          }
        }
      }
    }
  }
);

