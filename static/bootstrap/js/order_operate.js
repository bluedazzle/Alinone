
function order_print_all(){
    document.getElementById('all').focus();
    document.getElementById('all').contentWindow.print();
}

function jujueone(order_account){
    var r=confirm("您确定要取消订单么？？？");
    if(r==true){
        window.location.href="jujueone"+order_account;
    }
}


function jujueall(){
    var r=confirm("您确定要取消所有订单么？？？");
    if(r==true){
        window.location.href="jujueall";
    }
}


function platform_name(name){
    $('#platform_name').value(name);
}


//function yanzheng_limit(){
//    if(localStorage['time_count']){
//        var count = parseInt(localStorage['time_count']);
//        var countdwon = setInterval(CountDown(),1000);
//    }
//    else{
//        $('#yanzheng').click(function(){
//             var count = 30;
//             var countdown = setInterval(CountDown, 1000);
//        })
//    }
//    function CountDown() {
//        localStorage['time_count'] = count;
//        $("#yanzheng").attr("disabled", true);
//        $("#yanzheng").val("请等待 " + count + "秒");
//        if (count == 0) {
//            $("#yanzheng").val("获取验证码").removeAttr("disabled");
//            clearInterval(countdown);
//            localStorage['time_count'].clear();
//        }
//        count--;
//    }
//}
