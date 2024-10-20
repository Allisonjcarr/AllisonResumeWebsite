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
const data1 = {
    labels: devicesData.devices,
    datasets: [{
        label: 'Device Distribution',
        data: devicesData.counts
    }]
};
new Chart(ctx2, {
    type: 'doughnut',
    data: data1,
    options: {
        responsive: true
    }
});

const ctx3 = document.getElementById('browsersChart');
const data2 = {
    labels: browsersData.browsers,
    datasets: [{
        label: 'Browser Distribution',
        data: browsersData.counts
    }]
};
new Chart(ctx3, {
    type: 'doughnut',
    data: data2,
    options: {
        responsive: true
    }
});

fetch('https://unpkg.com/us-atlas/states-10m.json').then((r) => r.json()).then((us) => {
    const nation = ChartGeo.topojson.feature(us, us.objects.nation).features[0];
    const states = ChartGeo.topojson.feature(us, us.objects.states).features;

    console.log(stateData)


    const chart = new Chart(document.getElementById("usaTrafficChart").getContext("2d"), {
        type: 'choropleth',
        data: {
            labels: states.map((d) => d.properties.name),
            datasets: [{
                label: 'States',
                outline: nation,
                data: states.map((d) => ({
                    feature: d,
                    value: stateData[d.properties.name] ? stateData[d.properties.name] : 0
                })),
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: false
                },
            },
            scales: {
                projection: {
                    axis: 'x',
                    projection: 'albersUsa'
                },
                color: {
                    axis: 'x',
                    quantize: 5,
                    legend: {
                        position: 'bottom-right',
                        align: 'bottom'
                    },
                }
            },
        }
    });
});

fetch('https://unpkg.com/world-atlas/countries-50m.json').then((r) => r.json()).then((data) => {
    const countries = ChartGeo.topojson.feature(data, data.objects.countries).features;
    
    const chart = new Chart(document.getElementById("globalTrafficChart").getContext("2d"), {
        type: 'choropleth',
        data: {
            labels: countries.map((d) => d.properties.name),
            datasets: [{
                label: 'Countries',
                data: countries.map((d) => ({
                    feature: d,
                    value: countryData[d.properties.name] ? countryData[d.properties.name] : 0
                })),
            }]
        },
        options: {
            showOutline: true,
            showGraticule: true,
            plugins: {
                legend: {
                    display: false
                },
            },
            scales: {
                projection: {
                    axis: 'x',
                    projection: 'equalEarth'
                }
            }
        }
    });
});