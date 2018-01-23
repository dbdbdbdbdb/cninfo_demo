/**
 * Created by q8931 on 2017/7/23.
 */
function removeDuplicatedItem(ar) {
    console.log(ar)
    var ret = [];

    for (var i = 0, j = ar.length; i < j; i++) {
        if (ret.indexOf(ar[i]) === -1) {
            ret.push(ar[i]);
        }
    }
    console.log(ret)
    return ret;
}

var option = {
    title: {
        text: ''
    },
    //关掉旋转(...)？
    animation: false,
    animationDuration:0,
    addDataAnimation: false,
    //本系列特定的 tooltip 设定。
    tooltip: {},
    // 数据更新动画的时长。
    animationDurationUpdate: 0,
    // 数据更新动画的缓动效果。
    //animationEasingUpdate: 'quinticInOut',
    label: {
        normal: {
            show: true,
            textStyle: {
                fontSize: 12
            }
        }
    },
    legend: {
        x: "center",
        show: false,
        data: ["实体", "文本"]
    },
    markLine:{
                effect:{
                    loop:false,
                }
            },
    series: [

        {
            // 设置展示形式
            type: 'graph',
            // 图的布局
            layout: 'force',
            // 节点是否可拖拽，只在使用力引导布局的时候有用。
            // draggable: true,
            //节点标记的大小,可以设置成诸如 10 这样单一的数字，也可以用数组分开表示宽和高，例如 [20, 10] 表示标记宽为20，高为10。
            symbolSize: 45,
            //关闭旋转效果
            markLine:{
                effect:{
                    loop:false,
                }
            },
            // 将指定的节点以及其所有邻接节点高亮。
            focusNodeAdjacency: true,
            // 是否开启鼠标缩放和平移漫游
            roam: true,
            // 节点分类的类目，可选。
            // 如果节点有分类的话可以通过 data[i].category 指定每个节点的类目，类目的样式会被应用到节点样式上。
            // 图例也可以基于categories名字展现和筛选。
            categories: [{
                // 类目名称，用于和 legend 对应以及格式化 tooltip 的内容。
                name: '实体',
                itemStyle: {
                    normal: {
                        color: "#009800"
                    }
                }
            }, {
                name: '文本',
                itemStyle: {
                    normal: {
                        color: "#4592FF"
                    }
                }
            },{
                // 类目名称，用于和 legend 对应以及格式化 tooltip 的内容。
                name: '类别',
                itemStyle: {
                    normal: {
                        color: "red"
                    }
                }
            },],
            // source:边的源节点名称的字符串，也支持使用数字表示源节点的索引。
            // target:边的目标节点名称的字符串，也支持使用数字表示源节点的索引。
            // value:边的数值，可以在力引导布局中用于映射到边的长度。
            // label:标签

            // 图形上的文本标签相关设置，可用于说明图形的一些数据信息，比如值，名称等
            label: {
                normal: {
                    show: true,
                    textStyle: {
                        fontSize: 12
                    },
                }
            },
            // 力引导布局相关的配置项
            force: {
                // 节点之间的斥力因子。
                repulsion: 1000
            },
            edgeSymbolSize: [4, 50],
            edgeLabel: {
                normal: {
                    show: true,
                    // 该行报错,找不到middle!!!!标签位置:线的中点
                    // position:middle,
                    textStyle: {
                        fontSize: 10
                    },
                    // 标签内容格式器，支持字符串模板和回调函数两种形式,模板变量有 {a}、{b}、{c}，分别表示系列名，数据名，数据值。
                    formatter: "{c}"
                }
            },
            lineStyle: {
                normal: {
                    opacity: 0.9,
                    width: 1,
                    curveness: 0
                }
            }
        }
    ]
};


$(document).ready(function () {

    $.ajax({
        type: "POST",
            url: "/",
            data: {'search_type': 'init'},
            success: function(recommend_list) {
                $('input.completer').completer({
                    source: recommend_list,
                    suggest: true
                })
                console.log('recommend ready.');
            },
            error: function(error) {
                console.log(error);
            }
    })

    console.log("ready!");

    // 监听表单提交
    $('form').on('submit', function () {

        console.log("the form has been submitted");
        var form_id = this.id;
        console.log(form_id);
        // 抓取提交的input值
        inputv = $('#' + form_id + ' input');
        first = $('#' + form_id + ' input').val();
        second = form_id;
        third = $('#' + form_id + ' select').val();
        console.log(first, second, third);
        if (second === 'search1') {
            $.ajax({
                type: "POST",
                url: "/",
                data: {'str_to_solve': first, 'search_type': second},
                success: function (json_str) {
                    // 添加各年份按钮
                    console.log('success!');
                    $('#main-parent1').empty();
                    $('#main-parent1').append('<div id="main1" style="width:1200px;height: 600px;"></div>');
                    var myChart = echarts.init(document.getElementById('main1'));
                    myChart.setOption(option);
                    hearClick(myChart);
                    var data_json = JSON.parse(json_str);
                    year_arr = Object.keys(data_json);
                    console.log(year_arr[year_arr.length - 1]);
                    // console.log(data_json);
                    tmpdata=data_json[year_arr[year_arr.length - 1]].data;

                    tmpdata=removeDuplicatedItem(tmpdata);
                    console.log(tmpdata);

                    tmplink=data_json[year_arr[year_arr.length - 1]].links;

                    console.log(Object.prototype.toString.call(tmplink)) ;
                    tmplink=removeDuplicatedItem(tmplink);
                    console.log(tmplink);

                    myChart.setOption({
                        series: [{
                            //访问属性是通过.操作符完成的，但这要求属性名必须是一个有效的变量名.
                            // 如果属性名包含特殊字符，就必须用''括起来.
                            // 访问这个属性也无法使用.操作符，必须用['xxx']来访问
                            data: data_json[year_arr[year_arr.length - year_arr.length]].data,
                            links: data_json[year_arr[year_arr.length - year_arr.length]].links
                        }]
                    });
                    console.log('success!');
                    addYearButton(year_arr, data_json, myChart);
                    console.log(year_arr)
                },
                error: function (error) {
                    console.log(error)
                }
            });
        }
        if (second === 'search2') {
            $.ajax({
                type: "POST",
                url: "/",
                cache: false,
                data: {'str_to_solve': first, 'search_type': second, 'select': third},
                success: function (json_str) {
                    console.log('success');
                    console.log(typeof json_str);
                    // console.log(json_str)
                    json_list = JSON.parse(json_str);
                    console.log(Array.isArray(json_list));
                    crt_table(json_list);
                }
            })
        }
        if (second === 'search3') {
            entity_1 = inputv[0].value;
            entity_2 = inputv[1].value;
            $.ajax({
                type: "POST",
                url: "/",
                cache: false,
                data: {'search_type': second, 'entity1': entity_1, 'entity2': entity_2},
                success: function (json_str) {
                    console.log(json_str);
                    console.log('success');
                    json_list = JSON.parse(json_str);
                    relation_table(json_list);
                }
            })
        }
    });

});



function hearClick(myChart) {
    //监听双击事件,进行动态获取数据的处理
    myChart.on('dblclick', function (param) {
        //获取已生成图形的option
        var option = myChart.getOption();
        //获得所有节点数组
        var nodesOption = option.series[0].data;
        //获得所有连接的数组
        var linksOption = option.series[0].links;
        var data = param.data;
        // 数组第一个值不是根节点,所以不采用了
        // var first=  nodesOption[0].id;
        console.log(data.id);
        // console.log(nodesOption);
        // console.log(linksOption);
        function mergeArray(arr1, arr2) {
            var arr3 = [];
            for (var i in arr1) {
                var flag = false;
                for (var j in arr2) {
                    if (arr2[j].id === arr1[i].id) {
                        flag = true;
                        break;
                    }
                }
                if (!flag) arr3.push(arr1[i])
            }
            arr3 = arr3.concat(arr2);
            return arr3;
        }

        //判断是否为边或者字面值节点
        if (typeof data.id === 'undefined' || data.category === 1) {
            //如果id等于undefined或者是文本值,则不作交互处理
        } else {
            $.ajax({
                type: "POST",
                url: "/",
                data: {'str_to_solve': data.id, 'search_type': 'plus'},
                success: function (json_str) {
                    console.log(data.id, 'success');
                    var data_json = JSON.parse(json_str);
                    // 成功接收到对象
                    // console.log(data_json);
                    //判断data和links是不是数组
                    // console.log(Array.isArray(data_json.data))
                    nodesOption = mergeArray(nodesOption, data_json.data);
                    linksOption = linksOption.concat(data_json.links);
                    myChart.setOption({
                        series: [{
                            data: nodesOption,
                            links: linksOption
                        }]
                    })
                }
            })
        }
    });
    //监听单击事件,进行动态获取数据的处理
    myChart.on('click', function (param) {
        //获取已生成图形的option
        var option = myChart.getOption();
        //获得所有节点数组
        var nodesOption = option.series[0].data;
        //获得所有连接的数组
        var linksOption = option.series[0].links;
        var data = param.data;
        // 数组第一个值不是根节点,所以不采用了
        // var first=  nodesOption[0].id;
        console.log(data.id);
        // console.log(nodesOption);
        // console.log(linksOption);
        function mergeArray(arr1, arr2) {
            var arr3 = [];
            for (var i in arr1) {
                var flag = false;
                for (var j in arr2) {
                    if (arr2[j].id === arr1[i].id) {
                        flag = true;
                        break;
                    }
                }
                if (!flag) arr3.push(arr1[i])
            }
            arr3 = arr3.concat(arr2);
            return arr3;
        }

        //判断是否为边或者字面值节点
        if (typeof data.id === 'undefined' || data.category === 1 || data.category==0) {
            //如果id等于undefined或者是文本值或者是uri值,则不作交互处理
        } else {
            $.ajax({
                type: "POST",
                url: "/",
                data: {'str_to_solve': data.id, 'search_type': 'extend'},
                success: function (json_str) {
                    console.log(data.id, 'success');
                    var data_json = JSON.parse(json_str);
                    // 成功接收到对象
                    // console.log(data_json);
                    //判断data和links是不是数组
                    // console.log(Array.isArray(data_json.data))
                    nodesOption = mergeArray(nodesOption, data_json.data);
                    linksOption = linksOption.concat(data_json.links);
                    myChart.setOption({
                        series: [{
                            data: nodesOption,
                            links: linksOption
                        }]
                    })
                }
            })
        }
    });
}

function crt_table(json_list) {
    console.log(json_list);
    var data = json_list;
    $('#year-div').empty();
    $('#main2').empty().append('<div class="table-responsive"><table class="table table-bordered table-hover table-condensed" id="answer-table"></table></div>')
    var str = '';
    for (var i in data) {
        str += "<tr>";
        for (var j in data[i]) {
            str += "<td>" + data[i][j] + "</td>";
            //console.log(data[i][j])
        }
        str += "</tr>"
    }
    console.log(str);
    $('#answer-table').append(str)
}

function relation_table(json_list) {
    var data = json_list;
    console.log(data);
    $('#year-div').empty();
    $('#main3').empty().append('<div class="table-responsive"><table class="table table-bordered table-hover table-condensed" id="answer-table"></table></div>')
    var str = '';
    for (var i in data) {
        console.log(data[i]);
        str += "<tr>";
        for (var j in data[i]) {
            str += "<td>" + data[i][j].value + "</td>";
            //console.log(data[i][j])
        }
        str += "</tr>"
    }
    //console.log(str);
    $('#answer-table').append(str)
}

function addYearButton(arr, data_json, myChart) {
    $("div#year-div").empty().append('<div class="panel panel-info"><div class="panel-heading"><h3 class="panel-title">年份列表</h3>' +
        '</div><div class="panel-body"><div class="btn-group btn-group-sm center-block" role="group" id="year-btn" aria-label="year">' +
        '</div></div></div>');
    for (var i in arr) {
        $("#year-div #year-btn").append('<button type="button" class="btn btn-default" name="' + arr[i] + '">' + arr[i] + '</button>');
        console.log(i)
    }
    $("#year-div").find(".btn-group button").each(function () {
        $(this).bind("click", function () {
            var i = this.name;
            console.log(i);
            myChart.setOption({
                series: [{
                    data: data_json[i].data,
                    links: data_json[i].links
                }]
            })
        })
    })
}
