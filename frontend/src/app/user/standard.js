export function draw(ecValue, phValue, tempValue) {
    Highcharts.chart('standard-chart-ec', {
        chart: {
            marginTop: 40,
            inverted: true,
            marginLeft: 100,
            type: 'bullet'
        },
        title: {
            text: null
        },
        plotOptions: {
            series: {
                pointPadding: 0.35,
                borderWidth: 0,
                color: 'black',
                targetOptions: {
                    width: '200%'
                }
            }
        },
        credits: {
            enabled: false
        },
        exporting: {
            enabled: false
        },
        xAxis: {
            categories: ['<span class="standard-chart-title">EC</span><br/> uS/cm']
        },
        yAxis: {
            plotBands: [{
                from: 0,
                to: 800,
                color: '#C7E6FF'
            }, {
                from: 800,
                to: 2500,
                color: '#45BBFF'
            }, {
                from: 2500,
                to: 3500,
                color: '#5FA5FF  '
            }],
            title: null,
            gridLineWidth: 0
        },
        series: [{
            data: [{
                y: ecValue,
                target: 100
            }]
        }],
        tooltip: {
            pointFormat: '<b>{point.y}</b> (Ideal at {point.target})'
        },
        legend: {
            enabled: false
        }
    });

    Highcharts.chart('standard-chart-temp', {
        chart: {
            marginTop: 40,
            inverted: true,
            marginLeft: 100,
            type: 'bullet'
        },
        title: {
            text: null
        },
        plotOptions: {
            series: {
                pointPadding: 0.35,
                borderWidth: 0,
                color: 'black',
                targetOptions: {
                    width: '200%'
                }
            }
        },
        credits: {
            enabled: false
        },
        exporting: {
            enabled: false
        },
        xAxis: {
            categories: ['<span class="standard-chart-title">Temperature</span><br/><span>Celsius</span>']
        },
        yAxis: {
            plotBands: [{
                from: 0,
                to: 10,
                color: '#45BBFF'
            }, {
                from: 10,
                to: 28,
                color: '#C7E6FF'
            }, {
                from: 28,
                to: 40,
                color: '#5FA5FF'
            }],
            title: null,
            gridLineWidth: 0
        },
        series: [{
            data: [{
                y: tempValue,
                target: 16
            }]
        }],
        tooltip: {
            pointFormat: '<b>{point.y}</b> (Ideal at {point.target})'
        },
        legend: {
            enabled: false
        }
    });

    Highcharts.chart('standard-chart-ph', {
        chart: {
            marginTop: 40,
            inverted: true,
            marginLeft: 100,
            type: 'bullet'
        },
        title: {
            text: null
        },
        plotOptions: {
            series: {
                pointPadding: 0.35,
                borderWidth: 0,
                color: 'black',
                targetOptions: {
                    width: '200%'
                }
            }
        },
        credits: {
            enabled: false
        },
        exporting: {
            enabled: false
        },
        xAxis: {
            categories: ['<span class="standard-chart-title">pH</span><br/>']
        },
        yAxis: {
            plotBands: [{
                from: 0,
                to: 6.5,
                color: '#45BBFF'
            }, {
                from: 6.5,
                to: 8.5,
                color: '#C7E6FF'
            }, {
                from: 8.5,
                to: 14,
                color: '#5FA5FF'
            }],
            title: null,
            gridLineWidth: 0
        },
        series: [{
            data: [{
                y: phValue,
                target: 7
            }]
        }],
        tooltip: {
            pointFormat: '<b>{point.y}</b> (Ideal at {point.target})'
        },
        legend: {
            enabled: false
        }
    });
}
