
function drawBarChart(data) {

    var list = []
    var serArray = [];
    var cateArray = [];
    var dataArray = [];
    var setObj = {};
    var chrList = ['chr1', 'chr2', 'chr3'];
    var allList = [];


    for (var keyS in data) {
        //list.push({'name': keyS, 'data': [Number(data[keyS][1])]});
        list.push([keyS, Number(data[keyS][1])]);
    }

    list.sort(function(a, b) {
            var x = a[1];
            var y = b[1];
            if (x > y) return -1;
            if (x < y) return 1;
            return 0;
        });

    console.log(list)

    $('#bar_var').highcharts({
        chart: {
            type: 'column',
            backgroundColor:'rgba(255, 255, 255, 0.0)'
        },
        title: {
            text: 'TOP 20 of snp variance of the genotype'
        },
        subtitle: {
            text: ''
        },
        xAxis: {
            type: 'category',
            labels: {
                rotation: -45,
                style: {
                    fontSize: '13px',
                    fontFamily: 'Verdana, sans-serif'
                }
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Variance'
            }
        },
        legend: {
            enabled: false
        },
        tooltip: {
            pointFormat: 'Variance of Genotype: <b>{point.y:.1f}</b>',
        },
        series: [{
            name: 'Variance',
            data: list.slice(0,20),
            dataLabels: {
                enabled: true,
                rotation: -90,
                color: '#FFFFFF',
                align: 'right',
                x: 4,
                y: 10,
                style: {
                    fontSize: '13px',
                    fontFamily: 'Verdana, sans-serif',
                    textShadow: '0 0 3px black'
                }
            }
        }]
    });
}
    

