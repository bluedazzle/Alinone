/**
 * Created by root on 15-4-20.
 */
function check_login_form(){
    if($('#login_username').val() && $('#login_password').val()){
        $('#login_form').submit()
    }
    else{
        $('#username_warning').remove();
        $('#password_warning').remove();
        if(!$('#login_username').val()){
            $('#login_username').after("<p class='text-danger text-center' style='font-size: 14px;' id='username_warning'>用户名不能为空</p>");
        }
        if(!$('#login_password').val()){
            $('#login_password').after("<p class='text-danger text-center' style='font-size: 14px;' id='password_warning'>密码不能为空</p>");
        }
    }

}

function magic_number(data) {
    var user_online_number = $("#user_online_number");
    var order_today_number = $('#order_today_number');
    var order_all_number = $('#order_all_number');
    user_online_number.animate({count: data['user_online_number']}, {
        duration: 500,
        step: function() {
            user_online_number.text(String(Math.ceil(this.count)));
        }
    });
    order_today_number.animate({count: data['order_today_number']}, {
        duration: 500,
        step: function() {
            order_today_number.text(String(Math.ceil(this.count)));
        }
    });
    order_all_number.animate({count: data['order_all_number']}, {
        duration: 500,
        step: function() {
            order_all_number.text(String(Math.ceil(this.count)));
        }
    });
}

function update_count(){
    $.ajax({
        type: 'GET',
        url: 'update_count',
        data: '',
        success: function(data){
            if(data=='F'){
                return false
            }
            else{
                magic_number(JSON.parse(data));
                console.log(data)
            }
        }
    })
}

function pass_merchant(merchant_id){
    $.ajax({
        type: 'POST',
        url: 'pass_merchant',
        data: {'merchant_id': merchant_id,
               'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val()},
        success: function(data){
            if(data=='T'){
                $('#m'+merchant_id).remove()
            }
            else{
                return false;
            }
        }
    })
}

function reject_merchant(merchant_id){
    $.ajax({
        type: 'POST',
        url: 'reject_merchant',
        data: {'merchant_id': merchant_id,
               'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val()},
        success: function(data){
            if(data=='T'){
                $('#m'+merchant_id).remove()
            }
            else{
                return false;
            }
        }
    })
}

function submit_log_form(form_id){
    $('#'+form_id).submit();
}

function turn_page(url){
    var start_time = $('#start_time').val();
    var end_time = $('#end_time').val();
    var page = $("input[name='page']").val();
    window.location.href = url + "?start_time=" + start_time + "&end_time" + end_time + "&page=" + page;
}