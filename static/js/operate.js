
function getCookie(name) {
                    var cookieValue = null;
                    if (document.cookie && document.cookie != '') {
                        var cookies = document.cookie.split(';');
                        for (var i = 0; i < cookies.length; i++) {
                            var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                break;
                            }
                         }
                     }
                     return cookieValue;
                }

function jieshouone(order_account){
        $.ajax({
                        type: 'GET',
                        url: "jieshouone"+order_account,
                        data: '',
                        success: function(data) {
                            if (data == 'T') {
                                $('#i' + order_account).parent().parent().remove();
                                if($('tr').length == 1){
                                    window.location.href = 'operate_new'
                                }
                            }else if(data == 'C'){
                                alert('该单已被用户取消，请在已取消订单中查看');
                                clearInterval(countdown);
                                window.location.href = 'operate_new'
                            }else if(data != 'N' && data != 'F'){
                                var mess = '有' + data.toString() + '单已被用户取消，请在已取消订单中查看';
                                alert(mess);
                            }
                            else if(data == 'N'){
                                window.location.href = 'login_in'
                            }
                        },
                        dataType: 'json'
                    });
}


function jujueone(order_account){
    var r=confirm("您确定要取消订单么？？？");
    if(r==true){
        $.ajax({
                        type: 'GET',
                        url: "jujueone"+order_account,
                        data: '',
                        success: function(data) {
                            if (data == 'T') {
                                $('#i' + order_account).parent().parent().remove();
                                if($('tr').length == 1){
                                    window.location.href = 'operate_new'
                                }
                            }
                            else{
                                window.location.href = 'login_in'
                            }
                        },
                        dataType: 'json'
                    });
    }
}
function cancel_one(order_account){
    var r=confirm("您确定要撤销订单么？？？");
    if(r==true){
        $.ajax({
                        type: 'GET',
                        url: "jujueone"+order_account,
                        data: '',
                        success: function(data) {
                            if (data == 'T') {
                                    window.location.href = 'operate_get'
                            }
                            else{
                                window.location.href = 'login_in'
                            }
                        },
                        dataType: 'json'
                    });
    }
}

function jieshouall(){
    var r=confirm("您确定要接收所有订单么？？？");
    if(r==true){
        $.ajax({
                        type: 'GET',
                        url: "jieshouall",
                        data: '',
                        success: function(data) {
                            if (data == 'T') {
                                window.location.href = 'operate_new'
                            }
                            else if(data == 'C'){
                                alert('该单已被用户取消，请在已取消订单中查看');
                                clearInterval(countdown);
                                window.location.href = 'operate_new'
                            }else if(data != 'N' && data != 'F'){
                                var mess = '有' + data.toString() + '单已被用户取消，请在已取消订单中查看';
                                alert(mess);
                            }
                            else if(data == 'N'){
                                window.location.href = 'login_in'
                            }
                        },
                        dataType: 'json'
                    });
    }
}


function jujueall(){
    var r=confirm("您确定要取消所有订单么？？？");
    if(r==true){
        $.ajax({
                        type: 'GET',
                        url: "jujueall",
                        data: '',
                        success: function(data) {
                            if (data == 'T') {
                                window.location.href = 'operate_new'
                            }
                            else{
                                window.location.href = 'login_in'
                            }
                        },
                        dataType: 'json'
                    });
    }
}

//function cancel_all(){
//    var r=confirm("您确定要取消所有订单么？？？");
//    if(r==true){
//        $.ajax({
//                        type: 'GET',
//                        url: "jujueall",
//                        data: '',
//                        success: function(data) {
//                            if (data == 'T') {
//                                window.location.href = 'operate_get'
//                            }
//                            else{
//                                window.location.href = 'login_in'
//                            }
//                        },
//                        dataType: 'json'
//                    });
//    }
//}

function finish_one(order){
        $.ajax({
                        type: 'GET',
                        url: "finishone",
                        data: {'order': order},
                        success: function(data) {
                            if (data == 'T') {
                                window.location.href = 'operate_get'
                            }
                            else{
                                window.location.href = 'login_in'
                            }
                        },
                        dataType: 'json'
                    });
}


function finish_all(){
    var r=confirm("您确定要完成所有订单吗？");
    if(r==true){
        $.ajax({
                        type: 'GET',
                        url: "finishall",
                        data: '',
                        success: function(data) {
                            if (data == 'T') {
                                window.location.href = 'operate_get'
                            }
                            else{
                                window.location.href = 'login_in'
                            }
                        },
                        dataType: 'json'
                    });
    }
}

function platform_name(name){
    $('#platform_name').value(name);
}

