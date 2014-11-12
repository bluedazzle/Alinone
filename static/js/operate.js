
//function getCookie(name) {
//                    var cookieValue = null;
//                    if (document.cookie && document.cookie != '') {
//                        var cookies = document.cookie.split(';');
//                        for (var i = 0; i < cookies.length; i++) {
//                            var cookie = jQuery.trim(cookies[i]);
//                // Does this cookie string begin with the name we want?
//                            if (cookie.substring(0, name.length + 1) == (name + '=')) {
//                                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                                break;
//                            }
//                         }
//                     }
//                     return cookieValue;
//                }

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

