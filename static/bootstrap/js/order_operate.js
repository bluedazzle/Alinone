function order_print(order_alin_account){
//     document.getElementById(order_alin_account).focus();
//     var page = document.getElementById(order_alin_account);
//     page.contentWindow.print();
//     page.contentWindow.close();
    var LODOP=getLodop();
	 LODOP.PRINT_INIT("");
//	 LODOP.SET_PRINT_STYLE("FontSize",13);
//	 LODOP.SET_PRINT_STYLE("Bold",1);
//	 LODOP.ADD_PRINT_TEXT(50,231,260,39,"打印页面部分内容");
	 LODOP.ADD_PRINT_HTM(0,0,'100%','100%',document.getElementById(order_alin_account).innerHTML);
//     LODOP.SET_PRINT_PAGESIZE(1,580,2760,order_alin_account);
    LODOP.ADD_PRINT_TEXT(0,0,58,27,"新加文本");
    LODOP.SET_PRINT_PAGESIZE(0,5800,270,"A4");
    LODOP.PREVIEW();
//  LODOP.PRINT();
}

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
