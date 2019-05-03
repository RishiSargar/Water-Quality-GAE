export function draw(phValue) {
    var gaugeOptions = {
        chart: {
            type: 'solidgauge'
        },
        title: null,
        pane: {
            center: ['50%', '85%'],
            size: '140%',
            startAngle: -90,
            endAngle: 90,
            background: {
                backgroundColor: (Highcharts.theme && Highcharts.theme.background1) || '#EEE',
                innerRadius: '60%',
                outerRadius: '100%',
                shape: 'arc'
            }
        },
        tooltip: {
            enabled: false
        },
        yAxis: {
            lineWidth: 0,
            minorTickInterval: null,
            tickAmount: 1,
            title: {
                y: -70
            },
            labels: {
                y: 15
            },
            stops: [
                [0.3, '#FF8A6A'],
                [0.5, '#F9FC96'],
                [0.7, '#4BA2FF']
            ],
        },
        plotOptions: {
            solidgauge: {
                dataLabels: {
                    y: 5,
                    borderWidth: 0,
                    useHTML: true
                }
            }
        },
        exporting: {
            buttons: {
                contextButton: {
                    enabled: false
                }
            }
        },
    };

    var phAxis = Highcharts.chart('ph-chart', Highcharts.merge(gaugeOptions, {
        yAxis: {
            min: 0,
            max: 14,
            tickInterval: Math.floor(14 / 1000),
            title: {
                text: 'pH'
            },
        },
        credits: {
            enabled: false
        },
        series: [{
            name: 'pH',
            data: [phValue],
            dataLabels: {
                format: '<div style="text-align:center"><span style="font-size:25px;color:' +
                    ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y}</span><br/>' +
                    '<span style="font-size:12px;color:silver">pH</span></div>'
            },
            tooltip: {
                valueSuffix: ' pH'
            }
        }]
    }));
}
