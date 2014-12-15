function drawBubble(data) {
    
    var serArray = [];
    var chrList = ["chr1", "chr2", "chr3"];
    var list = [];


    for (var chr in chrList) {
        inObj = [chrList[chr], []]
            for (var keyS in data) {
                if (data[keyS][0] == chrList[chr]) {
                    inObj[1].push (
                            {'name': keyS, 'size': Number(data[keyS][1]) - 1000}
                            );
                }
            }
        serArray.push(inObj);
    }
    console.log(serArray)

    for (var keyS in serArray) {
        list.push({'name': serArray[keyS][0], 'children': serArray[keyS][1]});
    }

    var bArray = {'name': 'bubble', 'children': list};

    console.log(bArray)
    

    var svgWidth = 1000; // SVG領域の横幅
    var svgHeight = 1000;    // SVG領域の縦幅
    var diameter = 1000; // 一番大きい円のサイズ
    var color = ["none", "#ffa0a0", "#a0a0ff", "orange", "#ffe090", "#a0ff90", "cyan", "#ccc", "#ff8080", "#c0ffc0", "#4090ff"];
    var svg = d3.select("#bubble").append("svg")
        .attr("width", svgWidth).attr("height", svgHeight)
    var bubble = d3.layout.pack()
        .size([diameter, diameter]) // 表示サイズを指定
    var grp = svg.selectAll("g")    // グループを対象にする
        .data(bubble.nodes(classes(bArray)))  // データを読み込む
        .enter()
        .append("g")
        .attr("transform", function(d) {    // 円のX,Y座標を設定
            return "translate(" + d.x + "," + d.y + ")";
        })
    var circle = grp.append("circle")   // 円を生成する
        .attr("r", 0)   // 円を指定した半径にする
        .attr("fill", function(d,i){// 塗りの色を指定
            for (var chr in chrList) {
                if (d.packageName == chrList[chr]) {
                    console.log(chrList[chr])
                    return color[Number(chr) + 1];
                }
            }
            return color[i]
        })
    var text = grp.append("text")   // 文字を生成する
        .attr("font-size", "9pt")   // 文字のサイズを指定する
        .attr("fill", "black")  // 文字の塗りの色を指定する
        .attr("opacity", 0) // 不透明度を指定
        .style("text-anchor", "middle") // 円の座標の中央から表示するようにする
        .text(function(d) { return d.className; } ) // データの中のclassNameが地区名なので、それを出力
    // 階層化されたJSONデータをフラット化する (D3.js本家のを少し変更して利用)
    function classes(root) {
        var classes = [];
        function recurse(name, node) {
            if (node.children) node.children.forEach(function(child) { recurse(node.name, child); });
            else classes.push({packageName: name, className: node.name, value: node.size});
        }
        recurse(null, root);
        return {children: classes};
    }
    circle
        .transition()   // トランジション指定
        .duration(2000) // 2秒かけてアニメーション
        .attr("r", function(d){ // 円を指定した半径にする
            return d.r;
        })
    text
        .transition()   // トランジション指定
        .duration(2000) // 2秒かけてアニメーション
        .attr("opacity", 1.0)   // 文字の不透明を指定する
}
