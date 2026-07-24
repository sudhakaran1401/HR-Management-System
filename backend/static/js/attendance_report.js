document.addEventListener("DOMContentLoaded", function () {

    const chartCanvas = document.getElementById("statusChart");
    if (!chartCanvas) return;

    const params = new URLSearchParams(window.location.search);
    if (!params.get("month") && !params.get("year")) return;

    const url = chartCanvas.dataset.url + "?" + params.toString(); // ✅ dynamic URL

    fetch(url)
        .then(response => response.json())
        .then(data => {

            if (window.myChart) {
                window.myChart.destroy();
            }

            window.myChart = new Chart(chartCanvas, {
                type: "pie",
                data: {
                    labels: ["Present", "Leave", "Holiday"],
                    datasets: [{
                        data: [data.data[0], data.data[1], data.data[2]],
                        backgroundColor: [
                            "#198754",
                            "#dc3545",
                            "#0dcaf0"
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: "top" }
                    }
                }
            });

        });

});