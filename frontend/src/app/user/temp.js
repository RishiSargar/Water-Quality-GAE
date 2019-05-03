export function draw(tempValues, timestamps) {
    Highcharts.chart('temp-chart', {

        title: {
            text: 'Temperature'
        },
        yAxis: {
            title: {
                text: 'temperature'
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
            name: 'Temperature',
            data: tempValues
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
