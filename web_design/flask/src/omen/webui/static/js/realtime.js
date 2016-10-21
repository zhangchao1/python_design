var dom = document.getElementById("main");
var myChart = echarts.init(dom);
var type  = $("#time").val()
var date = [];
var data = [];
var map = new Map()
map = {
    '1m':[0.1,6,'seconds'],
    '5m':[0.5,30,'seconds'],
    '15m':[1,1,'minutes'],
    '30m':[1,1,'minutes'],
    '1h':[2,2,'minutes'],
}
function getAllWebsite(){
    $.ajax({
        url: '/api/get_all_website/',
        type: 'get',
        data: {
            'type':'all',
            'rangetime':20
        },
        datatype: "json",
        contenttype: 'application/json',
        success: function(msg) {
            var msg = jQuery.parseJSON(msg);
            if(msg.message == "not found" || msg.message=="empty value"){
                alert(msg.message)
            }else{
                var list = msg.message
                var li = "";
                $.each(list,function(index,array){ //遍历json数据列
                     if (index==0){
                         li =li+ "<option value=" +array +" selected='selected'>"+array+"</option>"
                     }
                    else{
                         li=li+"<option value="+array+">"+array+"</option>"
                     }
                });
                $("#api").append(li)

                if (window.location.hash){
                    var hash = window.location.hash.split("#")
                    $("#api").val(hash[1]);
                }else{
                    $("#api").change()
                }
                $("#time").change()
            }
        }
    });
}

function choose_type(){
    data = [];
    date = [];
    var now = moment();
    var type  = $("#time").val()
    var to,from;
    switch (type){
        case '1m':
           to = now.subtract(0, 'minutes').format('YYYY-MM-DD HH:mm:00');
           from = now.subtract(1, 'minutes').format('YYYY-MM-DD HH:mm:00');
           break;
        case '5m':
           to = now.subtract(0, 'minutes').format('YYYY-MM-DD HH:mm:00');
           from = now.subtract(5, 'minutes').format('YYYY-MM-DD HH:mm:00');
           break;
        case '15m':
           to = now.subtract(0, 'minutes').format('YYYY-MM-DD HH:mm:00');
           from = now.subtract(15, 'minutes').format('YYYY-MM-DD HH:mm:00');
           break;
        case '30m':
           to = now.subtract(0, 'minutes').format('YYYY-MM-DD HH:mm:00');
           from = now.subtract(30, 'minutes').format('YYYY-MM-DD HH:mm:00');
           break;
        case '1h':
           to = now.subtract(0, 'minutes').format('YYYY-MM-DD HH:mm:00');
           from = now.subtract(60, 'minutes').format('YYYY-MM-DD HH:mm:00');
           break;
        case '4h':
           to = now.subtract(0, 'minutes').format('YYYY-MM-DD HH:mm:00');
           from = now.subtract(60 * 4, 'minutes').format('YYYY-MM-DD HH:mm:00');
           break
        case '1d':
           to = now.subtract(0, 'minutes').format('YYYY-MM-DD HH:mm:00');
           from = now.subtract(24, 'hours').format('YYYY-MM-DD HH:mm:00');
           break
        case '4d':
           to = now.subtract(0, 'minutes').format('YYYY-MM-DD HH:mm:00');
           from = now.subtract(4, 'days').format('YYYY-MM-DD HH:mm:00');
           break
        case '7d':
           to = now.subtract(0, 'minutes').format('YYYY-MM-DD HH:mm:00');
           from = now.subtract(7, 'days').format('YYYY-MM-DD HH:mm:00');
           break
    }
    loaddata(from, to,type);
}
$("#api").change(function(){
    window.location.hash =  $("#api").val();
    choose_type()
})

var time;
    $("#time").change(function(){
    choose_type()
    if(time){
        clearInterval(time)
    }
    console.log($(this).val(), map[$(this).val()][0]);
    time = setInterval(function () {
    autoRefresh()
    }, 1000 * 60 * map[$(this).val()][0]);

})

getAllWebsite()
function autoRefresh(){
    var lastdate = moment().format('YYYY-MM-DD ') + date[data.length - 1] + ':00';
    var type  = $("#time").val()
    var from = moment(lastdate).add(map[type][1], map[type][2]).format('YYYY-MM-DD HH:mm:ss');
    var to = moment(from).add(map[type][1], map[type][2]).format('YYYY-MM-DD HH:mm:ss');
    var type  = $("#time").val()
    //console.log(lastdate)
    //console.log(to)
    if (type == '15m' || type =='30m'||type=='1m'||type=='5m'){
        loaddata(from, to,type,true);
    }
}


function drawing(legend_data){
    var option = {
        title: {
            text: '站点实时监控'
        },
        tooltip : {
            trigger: 'axis'
        },
        legend: {
            data: legend_data
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis : [
        {
            type : 'category',
            boundaryGap : false,
            data : date
        }
        ],
        yAxis : [
        {
            type : 'value'
        }
        ],
        series : [
        {
            name: '访问量',
            type:'line',
            stack: '总量',
            data: data
        },
        ]
    }
    // 为echarts对象加载数据
    myChart.setOption(option);

}
function loaddata(from, to, type,shift=false){
    var apiname =  $("#api").val();

    $.ajax({
        url: '/api/search_api_visit/',
        type: 'get',
        data: {
            'apiname': apiname,
            'from': from,
            'to': to,
            'type':type
        },
        datatype: "json",
        contenttype: 'application/json',
        success: function(msg) {
            var msg = eval(msg);
            if(msg.message == "not found" || msg.message=="empty value"){
                alert(msg.message)
            }else{
                for(var i = 0; i< msg.length; i++){
                    var temp = msg[i].split("?");
                    date.push(temp[0]);
                    data.push(temp[1]);

                    if(shift){
                        date.shift();
                        data.shift();
                    }
                }
                console.log(from, to, date, data);
                drawing()
            }
        }
    });
}
