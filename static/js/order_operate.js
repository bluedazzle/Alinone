
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


