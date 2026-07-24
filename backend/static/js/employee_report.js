(function () {

  const ctx = document.getElementById("joinChart");
  if (!ctx) return;

  const params = new URLSearchParams(window.location.search);
  const url = ctx.dataset.url + "?" + params.toString();

  fetch(url)
    .then(r => r.json())
    .then(payload => {

      new Chart(ctx, {
        type: "bar",
        data: {
          labels: payload.labels,
          datasets: [{
            label: "Employees Joined",
            data: payload.data,
            backgroundColor: "#0d6efd"
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false
        }
      });

    });

})();