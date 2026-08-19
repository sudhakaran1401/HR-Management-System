document.addEventListener("DOMContentLoaded", function () {


    const ctx = document.getElementById('leaveChart');
 
    const approved = Number(ctx.dataset.approved || 0);
    const pending = Number(ctx.dataset.pending || 0);
    const rejected = Number(ctx.dataset.rejected || 0);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Approved', 'Pending', 'Rejected'],
            datasets: [{
                label: 'Leave Requests',
                data: [approved, pending, rejected],
                backgroundColor: [
                    '#198754',  
                    '#ffc107',  
                    '#dc3545'   
                ],
                borderRadius: 6,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });

});
