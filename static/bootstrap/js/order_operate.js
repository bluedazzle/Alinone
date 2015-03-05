
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
    var r=confirm("您确定要取消所有订单么？？？?");
    if(r==true){
        window.location.href="jujueall";
    }
}


function platform_name(name){
    $('#platform_name').value(name);
}

function post(URL, PARAMS) {
    var temp = document.createElement("form");
    temp.action = URL;
    temp.method = "post";
    temp.style.display = "none";
    for (var x in PARAMS) {
        var opt = document.createElement("textarea");
        opt.name = x;
        opt.value = PARAMS[x];
        // alert(opt.name)
        temp.appendChild(opt);
    }
    document.body.appendChild(temp);
    temp.submit();
    return temp;
}
