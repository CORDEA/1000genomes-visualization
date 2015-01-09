function drawPieChart(name, item) {
    var data = [];

    for (var keyS in item) {
        if (keyS != "RESULT") {
            data.push([keyS, item[keyS]]);
        }
    }

    if (name == 'spc') {
            title = "Super population"
    } else {
            title = "Population"
    }

    $('#' + name + 'container').highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: 1,//null,
            plotShadow: false
        },
        title: {
            text: 'Prediction Result: ' + title
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                    }
                }
            }
        },
        series: [{
            type: 'pie',
            name: 'probability',
            data: data
        }]
    });
}
