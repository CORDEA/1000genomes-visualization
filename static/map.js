function drawWMap(markersList, populationTable, c){
    var map = 'world_mill_en'
    var norfunc = 'polynomial'
    var marker = markersList[0]
    var mValue = markersList[1][c]
    var markerStyle = {
                    initial: {
                        r: 11
                        },
                    selected: {
                        fill: 'yellow'
                        }
                    }
    console.log(c);
    console.log(mValue)

    $('#map').vectorMap({
        map: map,
        backgroundColor: "#f9f9f9",
        zoomOnScroll: false,
        markers: marker,
        markerStyle: markerStyle,
        series: {

        markers: [{
            attribute: 'fill',
            scale: ['#DEEBF7', '#021222'],
            values: mValue,
            min: 0,
            max: 100
            //}],
            //regions: [{
            //scale: ['#75a567'],
            //attribute: 'fill',
            //values: data,
            }]
        },
        regionStyle: {
            initial: {
                fill: '#c5c5c5'
            },
            hover: {
                "fill-opacity": 0.8
            }
        },
        onRegionLabelShow: function(e, el, code){
            el.html(el.html());
        },
        onMarkerClick: function(e, index, pie){
            var iName = marker[index].name
            markerClick(iName, marker[index].latLng, mValue[index], marker[index].pie, populationTable)
        }
    });
}

function mapSelect(mL, populationTable, c) {
    $('#mapselect').click(function () {
        $('#map').empty();
        drawWMap(mL, populationTable, c);
        //drawPolarChart(spc, c);
        //drawbarChart(mL, c)
    });
}

function markerClick(name, data, value, pie, populationTable) {
    flag = slide();
    var time = 0;
    if (flag) {
        time = 300;
    }
    
    setTimeout (
        function() {
            $('#detailth').empty();

            var tableRef = document.getElementById('detailtable');
            var freqTable = document.getElementById('freqtable');
            console.log(populationTable);
            tableRef.rows[0].cells[1].innerText = name
            tableRef.rows[1].cells[1].innerText = populationTable[name][0]
            tableRef.rows[2].cells[1].innerText = populationTable[name][1]
            tableRef.rows[3].cells[1].innerText = value + " %"
            var count = pie.length;
            for (var i = 0; i < count; i++) {
                freqTable.rows[i+1].cells[1].innerText = pie[i]
            }
            //document.getElementById('content').style.display="block"
            //console.log(pie);
            //drawPolarChart(pie);
            $("#content").slideToggle("fast");
        }
    ,time);
}

function slide() {
    if ($('#content').css('display') == "block") {
        $("#content").slideToggle("fast");
        console.log("close");

        return true;
    } else {
        return false;   
    };
}

