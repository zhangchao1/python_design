var myChart = echarts.init(document.getElementById('main'));
myChart.showLoading({
    text : 'Loading',
    effect : 'spin',
    textStyle : {
            fontSize : 30
        }
});
var time;
function render(data){
    var option = {
        backgroundColor: '#1b1b1b',
        color: [
            // 'rgba(255, 255, 255, 0.8)',
            'rgba(196, 223, 253, 0.8)',
            // 'rgba(37, 140, 249, 0.8)'
            'rgba(14,240,242, 0.8)',
            // 'rgba(30,108,204, 0.8)',
            'rgba(7,120,249, 0.8)'

        ],
        title : {
            text: data.total,
            subtext: '实时访问量',
            x:'center',
            textStyle : {
                color: '#fff',
                fontSize: 50,
                fontWeight: 'bolder',
            }
        },
        legend: {
            orient: 'vertical',
            x:'left',
            data:['强','中','弱'],
            textStyle : {
                color: '#fff'
            }
        },
        toolbox: {
            show : true,
            orient : 'vertical',
            x: 'right',
            y: 'center',
            feature : {
                mark : {show: true},
                dataView : {show: true, readOnly: false},
                restore : {show: true},
                saveAsImage : {show: true}
            }
        },
        series : [
        {
            name: '弱',
            type: 'map',
            mapType: 'china',
            itemStyle:{
                normal:{
                    borderColor:'rgba(100,149,237,1)',
                    borderWidth:1.5,
                    areaStyle:{
                        color: '#1b1b1b'
                    }
                }
            },
            data : [],
            markPoint : {
                symbol : 'circle',
                symbolSize: 7,
                large: true,
                effect : {
                    show: true
                },
                data : data.data.low
            }
        },
        {
            name: '中',
            type: 'map',
            mapType: 'china',
            data : [],
            markPoint : {
                symbol : 'circle',
                symbolSize: 17,
                large: true,
                effect : {
                    show: true
                },
                data : data.data.middle
            }
        },
        {
            name: '强',
            type: 'map',
            mapType: 'china',
            hoverable: false,
            roam:true,
            data : [],
            markPoint : {
                symbol : 'circle',
                symbolSize: 27,
                large: true,
                effect : {
                    show: true
                },
                data : data.data.high
            }
        }
        ]
    };

    myChart.hideLoading();
    myChart.setOption(option);

    time = setTimeout(function (){
        loadData();
    }, 1000 * 10);
}

$("#visit").change(function(){
    clearTimeout(time)
    loadData();
}).change()

function loadData(){
    console.log(new Date())
    var type = $("#visit").val()
    $.ajax({
        url: '/api/all_china_web_visit/',
        type: 'get',
        data: {
            'type':type
        },
        datatype: "json",
        contenttype: 'application/json',
        success: function(response) {
            var result = jQuery.parseJSON(response);
            if(result.is_success === true){
                render(result)
            }else{
            }
        }
    });
}


