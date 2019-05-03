export function draw(ecValues, timestamps) {
    Highcharts.chart('ec-chart', {
        title: {
            text: 'Electrical Conductivity'
        },
        yAxis: {
            title: {
                text: 'ec'
            }
        },
        xAxis:{
            title:{
                text: 'timestamp'
            },
            categories: timestamps
        },
        legend: {
            enabled: false
        },
        series: [{
            name: 'EC',
            data: ecValues
        }],
        responsive: {
            rules: [{
                condition: {
                    maxWidth: 500
                },
                chartOptions: {
                    legend: {
                        layout: 'horizontal',
                        align: 'center',
                        verticalAlign: 'bottom'
                    }
                }
            }]
        },
        exporting: {
            buttons: {
                contextButton: {
                    enabled: false
                }
            }
        },
        credits: {
            enabled: false
        }
    });
}