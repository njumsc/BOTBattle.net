function Timer(time) {
    var timer = null;
    var t = time;
    var m = 0;
    var s = 0;
    m = Math.floor(t / 60 % 60);
    m < 10 && (m = '0' + m);
    s = Math.floor(t % 60);
    function countDown() {
        s--;
        s < 10 && (s = '0' + s);
        if (s.length >= 3) {
            s = 59;
            m = "0" + (Number(m) - 1);
        }
        if (m.length >= 3) {
            m = '00';
            s = '00';
            clearInterval(timer);
        }
        $('#remainTime').html(m+":"+s)
        if (m == 0 && s == 0){
            clearInterval(timer);
            // console.log("cleared");
            refreshStatus();
        }
    }
    timer = setInterval(countDown, 1000);
    // console.log("start timer " + time);
}
var historyData = {
    type: 'line',
    data: {
        labels: ['1', '2', '3'],
        datasets: [{
            label: '黄金点',
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: [32.7, 19.3, 10.4],
            fill: false,
        }]
    },
    options: {
        legend: false,
        responsive: true,
        title: {
            display: true,
            text: '黄金点历史'
        },
        tooltips: {
            mode: 'index',
            intersect: true
        },
        scales: {
            xAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: '回合数'
                }
            }],
            yAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: '数值'
                },
                ticks: {
                    suggestedMin: 0,
                    suggestedMax: 20,
                }
            }]
        }
    },
    customOption: {
        amount: 10,
        history: []
    }
};
var rankData = {
    type: 'horizontalBar',
    data: {
        labels: ['homo', 'van', 'billy', 'banana'],
        datasets: [{
            label: '分数',
            backgroundColor: 'rgb(0, 123, 255)',
            borderColor: 'rgb(0, 123, 255)',
            data: [107, 35, 1, -10],
            fill: false,
        }]
    },
    options: {
        elements: {
            rectangle: {
                borderWidth: 2,
            }
        },
        maintainAspectRatio: false,
        responsive: true,
        legend: false,
        title: {
            display: true,
            text: '排行榜'
        },
        scales: {
            xAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: '分数'
                },
                ticks: {
                    suggestedMin: 0,
                    suggestedMax: 20,
                }
            }],
            yAxes: [{
                display: true,
                scaleLabel: {
                    display: false,
                    labelString: '用户名'
                },
            }]
        }
    },
    customOption: {
        lastLength: 4,
        lastScore: 0
    }
};
function refreshHistory(){
    var len = historyData.customOption.history.length;
    var i = 0;
    var i_start = historyData.customOption.amount;
    if (i_start >= len || i_start == 0){
        i_start = 0;
    }else{
        i_start = len - i_start;
    }
    historyData.data.labels = [];
    historyData.data.datasets[0].data = [];
    for (i = i_start; i < len; i++){
        historyData.data.labels.push(i + 1);
        historyData.data.datasets[0].data.push(historyData.customOption.history[i]);
    }
    // prompt_info("Last goldennum:"+historyData.customOption.history[len-1], 2000);
    window.myLineHistory.update();
}
function refreshRank(scores){
    let userCount = Object.keys(scores).length;
    let scoreLast = scores[getCookie('username')];
    if (scoreLast) {
        let scoreGain = scoreLast - rankData.customOption.lastScore;
        prompt_info(`你在上回合获得了 ${scoreGain} 分. 当前总分 ${scoreLast} 分.`, 2000);
        rankData.customOption.lastScore = scoreLast;
    }
    rankData.data.labels = [];
    rankData.data.datasets[0].data = [];
    for (let [name, score] of Object.entries(scores).sort((a, b) => b[1] - a[1])){
        rankData.data.labels.push(name);
        rankData.data.datasets[0].data.push(score);
    }
    if (rankData.customOption.lastLength == userCount){
        window.myLineRank.update();
    } else {
        rankData.customOption.lastLength = userCount;
        $("#rankDiv").attr("style", `height: ${50 * userCount}px`)
        window.myLineRank.destroy();
        let ctxRank = document.getElementById('rankChart').getContext('2d');
        window.myLineRank = new Chart(ctxRank, rankData);
    }
}
function refreshStatus() {
    let json = { roomid: getCookie("roomid") }
    $.get("roomStatus/", json, function(data, status) {
        if (data == "on") {
            $.get("getStatus/", json, function(data, status) {
                let json = JSON.parse(data);
                // console.log(json);
                if (json.status == "success") {
                    historyData.customOption.history = json.history.goldenNums;
                    refreshHistory();
                    refreshRank(json.scores);
                    Timer(json.time + 1);
                } else {
                    console.log(json.status);
                    prompt_fail("未知错误, 尝试重连至服务器", 5000);
                    Timer(7);
                }
            })
        }
    })
}
$(document).ready(function() {
    $.get('userStatus/', function(data, status){
        if (data != "No User Log In"){
            $('#pUsername').html("当前登陆：" + data)
            $('#login-panel').css("display", "none")
            $('#user-info').css("display", "block")
            setCookie("username", data, 1);
        }
    })
    $('#pRoomid').html(getCookie('roomid'))
    var ctxHistory = document.getElementById('historyChart').getContext('2d');
    window.myLineHistory = new Chart(ctxHistory, historyData);
    var ctxRank = document.getElementById('rankChart').getContext('2d');
    window.myLineRank = new Chart(ctxRank, rankData);
    Timer(1);
})
function tryChgLen(len){
    historyData.customOption.amount = len;
    refreshHistory();
    // console.log("set " + len);
}
$('#setLenBtn1').click(
    function tryChg(){
        tryChgLen(10);
    }
)
$('#setLenBtn2').click(
    function tryChg(){
        tryChgLen(30);
    }
)
$('#setLenBtn3').click(
    function tryChg(){
        tryChgLen(100);
    }
)
$('#setLenBtn4').click(
    function tryChg(){
        tryChgLen(0);
    }
)
$('#setRoomBtn').click(
    function trySetRoom() {
        var roomid = $('input[name="roomid"]').val();
        var json = {"roomid":roomid}
        // console.log(roomid);
        $.get('roomStatus/', json, function(data, status){
            if (data == "on"){
                setCookie('roomid', roomid, 1);
                $('#pRoomid').html(roomid)
                prompt_success("成功加入房间", 2000);
                location.reload();
            }else{
                prompt_fail("房间已关闭", 2000);
            }
        })
    }
)
$('#loginBtn').click(
    function tryLogin() {
        var uname = $('input[name="username"]').val();
        var json = {"name":uname}
        // console.log(json);
        $.get('userReg/',json,function(data,status){
            // console.log(data);
            if (data == "User register success" || data == "User login success"){
                setCookie("username", data, 1);
                $('#pUsername').html("当前登陆：" + uname)
                $('#login-panel').css("display", "none")
                $('#user-info').css("display", "block")
            }
            switch(data){
                case "User exist":
                    prompt_info("用户已存在", 2000);
                    break;
                case "User login success":
                    prompt_success("登陆成功", 2000);
                    break;
                case "User register success":
                    prompt_success("注册成功", 2000);
                    break;
                case "You have logged in":
                    prompt_info("已经登陆, 如需再登陆, 尝试注销", 2000);
                    break;
                default:
                    prompt_fail(data, 2000);
            }
        })
    }
)
$('#logoutBtn').click(
    function tryLogout() {
        $.get('userOut/', function(data, status){
            removeCookie("username");
            switch(data){
                case "No login":
                    prompt_fail("未登录, 请先登录再注销", 2000);
                    break;
                case "Logout success":
                    prompt_success("注销成功", 2000);
                    break;
                default:
                    console.log(data);
                    prompt_fail("未知错误", 2000);
            }
        })
        $('#pUsername').html("")
        $('#login-panel').css("display", "block")
        $('#user-info').css("display", "none")
    }
)
$('#submitNumBtn').click(
    function sumbitNum(){
        var num1 = $('input[name="num1"]').val();
        var num2 = $('input[name="num2"]').val();
        var roomid = getCookie("roomid");
        var json = {"roomid":roomid,"num1":num1,"num2":num2}
        // console.log(json);
        $.get('userAct/',json,function(data,status){
            switch(data){
                case "Numbers overflow":
                    prompt_fail("数字溢出, 请检查范围", 2000);
                    break;
                case "Upload success":
                    prompt_success("提交成功", 2000);
                    break;
                case "No login":
                    prompt_fail("未登录, 请先登录", 2000);
                    break;
                default:
                    prompt_fail(data, 2000);
            }
        })
    }
)

