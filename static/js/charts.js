const ctx1 = document.getElementById('visitsOverTimeChart');

new Chart(ctx1, {
    type: 'line',
    data: {
        labels: visitsOverTimeData.visit_dates,
        datasets: [{
            label: 'Website Visits (by hour)',
            data: visitsOverTimeData.visit_data,
            borderWidth: 1,
            borderColor: 'purple',
            backgroundColor: 'rgba(128, 0, 128, 0.5)',
            fill: true
        }]
    },
    options: {
        scales: {
            x: {
                display: false
            },
            y: {
                beginAtZero: true
            }
        },
    }
});

const ctx2 = document.getElementById('devicesChart');
const data = {
    labels: devicesData.devices,
    datasets: [{
        label: 'Device Distribution',
        data: devicesData.counts
    }]
};
new Chart(ctx2, {
    type: 'doughnut',
    data: data,
    options: {
        responsive: true
    }
});