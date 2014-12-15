function drawChart(key, item){
    $('#piebox').empty();
    var canvas = document.createElement('canvas');
    document.getElementById('piebox').appendChild(canvas);
    var ctx  = canvas.getContext('2d');

    var data = [
        {
            value: item[0],
            color: "#F7464A",
            label: "Allele: 1|1"
        },
        {
            value: item[1],
            color: "#46BFBD",
            label: "Allele: 0|0"
        },
        {
            value: item[2],
            color: "#FDB45C",
            label: "Allele: 1|0"
        },
        {
            value: item[3],
            color: "#949FB1",
            label: "Allele: 0|1"
        }
    ]
    new Chart(ctx).Doughnut(data);
}

function drawBarChart(item, c) {
   
    $('#barbox').empty();
    var canvas = document.createElement('canvas');
    canvas.width = 800;
    document.getElementById('barbox').appendChild(canvas);
    var ctx  = canvas.getContext('2d');

    var label = [];
    var value = [];

    for (var keyS in item[0]) {
        label.push( item[0][keyS]["name"] );
        value.push( item[0][keyS]["pie"][c]);
    }

    console.log(value);

    var data = {
        labels: label,
        datasets: [
            {
                label: "dataset",
                fillColor: "rgba(151,187,205,0.5)",
                strokeColor: "rgba(151,187,205,0.8)",
                highlightFill: "rgba(151,187,205,0.75)",
                highlightStroke: "rgba(151,187,205,1)",
                data: value
            }
        ]
    }

    var barChart = new Chart(ctx).Bar(data, {
        scaleLabel: "<%=value%>",
        scaleFontFamily: "'Verdana', 'Arial', sans-serif",
        showTooltips: false,
        barShowStroke: false
    });
}


function drawStackChart(item, ref, alt) {
    var key = [];
    var vRR = [];
    var vAA = [];
    var vRA = [];
    var vEE = [];

    var sitem = item.sort(function (a,b){return (a[0]-b[0]);});

    for (var keyS in sitem) {
        key.push(sitem[keyS][1]);
        vRR.push(sitem[keyS][2][0]);
        vAA.push(sitem[keyS][2][1]);
        vRA.push(sitem[keyS][2][2]);
        vEE.push(sitem[keyS][2][3]);
    }

    $('#barbox').highcharts({
        chart: {
            type: 'column',
            backgroundColor: 'rgba(255,255,255,0.0)'
        },
        title: {
            text: 'Stacked column chart in each ethnic group'
        },
        xAxis: {
            categories: key
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Total genetic variation'
            }
        },
        tooltip: {
            pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.percentage:.0f}%)<br/>',
            shared: true
        },
        plotOptions: {
            column: {
                stacking: 'percent'
            }
        },
            series: [{
            name: ref + '|' + ref,
            data: vRR
        }, {
            name: alt + '|' + alt,
            data: vAA
        }, {
            name: ref + '|' + alt,
            data: vRA
        }, {
            name: '-|-',
            data: vEE
        }]
    });
}

function drawSPCChart(item, ref, alt) {
    console.log(item);
    var key = [];
    var vRR = [];
    var vAA = [];
    var vRA = [];
    var vEE = [];

    sortList = ["SAS", "EAS", "AFR", "AMR", "EUR"];

    for (var keyS in sortList) {
        key.push(sortList[keyS]);
        vRR.push(item[sortList[keyS]][0]);
        vAA.push(item[sortList[keyS]][1]);
        vRA.push(item[sortList[keyS]][2]);
        vEE.push(item[sortList[keyS]][3]);
    }

    $('#spcbox').highcharts({
        chart: {
            type: 'column',
            backgroundColor: 'rgba(255,255,255,0.0)'
        },
        title: {
            text: 'Stacked column chart in super population'
        },
        xAxis: {
            categories: key
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Total genetic variation'
            }
        },
        tooltip: {
            pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.percentage:.0f}%)<br/>',
            shared: true
        },
        plotOptions: {
            column: {
                stacking: 'percent'
            }
        },
            series: [{
            name: ref + '|' + ref,
            data: vRR
        }, {
            name: alt + '|' + alt,
            data: vAA
        }, {
            name: ref + '|' + alt,
            data: vRA
        }, {
            name: '-|-',
            data: vEE
        }]
    });
}


function drawPolarChart(item, c) {
   
    $('#piebox').empty();
    var canvas = document.createElement('canvas');
    canvas.width = 150;
    canvas.height = 150;
    document.getElementById('piebox').appendChild(canvas);
    var ctx  = canvas.getContext('2d');

    var data = [
        {
            value: item["AFR"][c],
            color:"#F7464A",
            highlight: "#FF5A5E",
            label: "AFR"
        },
        {
            value: item["AMR"][c],
            color: "#46BFBD",
            highlight: "#5AD3D1",
            label: "AMR"
        },
        {
            value: item["ASN"][c],
            color: "#FDB45C",
            highlight: "#FFC870",
            label: "ASN"
        },
        {
            value: item["EUR"][c],
            color: "#949FB1",
            highlight: "#A8B3C5",
            label: "EUR"
        },
    ];

    new Chart(ctx).PolarArea(data, {
        segmentStrokeColor: "#000000",
        scaleFontFamily: "'Verdana', 'Arial', sans-serif"
    });
}


