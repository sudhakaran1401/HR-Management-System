
(function () {

  const ctx = document.getElementById("salaryChart");
  if (!ctx) return;

  const params = new URLSearchParams(window.location.search);
  const url = ctx.dataset.url + "?" + params.toString();

  fetch(url)
    .then(r => r.json())
    .then(payload => {
      new Chart(ctx, {
        type: "line",
        data: {
          labels: payload.labels,
          datasets: [{
            label: "Total Net Pay",
            data: payload.data,
            borderWidth: 2,
            tension: 0.3
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false
        }
      });
    });

})();