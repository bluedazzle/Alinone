# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
import AlinApi.method
from django.http import HttpResponse
from AlinApi.models import *
from django.contrib.auth.decorators import login_required
from auth import *
from CronOrder.models import *
import json
import hashlib
import datetime
import time


# Create your views here.
# 登录验证函数
@csrf_exempt
def login_in(request):
    if 'user_name' in request.POST and request.POST['user_name'] and 'password' in request.POST and request.POST['password']:
        user_name = request.POST['user_name']
        password = request.POST['password']
        try:
            user = Merchant.objects.get(alin_account=user_name)
            if user.check_password(password):
                request.session['username'] = user_name
                return HttpResponseRedirect("/merchant/operate_new")
            else:
                return render_to_response('login_page.html', {'flag': 1})
        except Merchant.DoesNotExist:
            return render_to_response('login_page.html', {'flag': 1})
    else:
        return render_to_response('login_page.html')


#登出函数
def login_out(request):
    del request.session['username']
    return HttpResponseRedirect("login_in")


#忘记密码操作
def forget_password(request):
    if request.method == 'GET':
        return render_to_response('forget_password.html')
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        verify = request.POST.get('verify')
        if phone and verify and password and len(phone) == 11:
            phone_verify = PhoneVerify.objects.get(phone=phone, verify_code=verify)
            if phone_verify:
                update_time = phone_verify.update_time
                if (update_time.replace(tzinfo=None) + datetime.timedelta(minutes=30)) < \
                        datetime.datetime.utcnow():
                    return render_to_response('register.html', {'phone': phone,
                                                                'fault1': 'T'})
                else:
                    merchant = Merchant.objects.get(alin_account=phone)
                    merchant.password = password
                    merchant.save()
                    request.session['username'] = phone
                    phone_verify.delete()
                    return HttpResponseRedirect("/merchant/operate_new")
            else:
                return render_to_response('register.html', {'phone': phone,
                                                            'fault3': '2'})


#忘记密码获取验证码
def forget_password_verify(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        merchant_have = Merchant.objects.get(alin_account=phone)
        if merchant_have:
            req = AlinApi.method.createverfiycode(phone)
            return HttpResponse(json.dumps("OK"), content_type="application/json")
    return HttpResponse(json.dumps("False"), content_type="application/json")


#注册
@csrf_exempt
def register(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        merchant_name = request.POST.get('merchant_name')
        phone = request.POST.get('phone')
        verify = request.POST.get('verify')
        if password and merchant_name and phone and verify and len(phone) == 11:
            user_test = Merchant.objects.get(alin_account=phone)
            if user_test:
                return render_to_response('register.html', {'phone': phone, 'merchant_name': merchant_name,
                                                            'fault2': 'T'})
            phone_verify = PhoneVerify.objects.get(phone=phone, verify_code=verify)
            if phone_verify:
                update_time = phone_verify.update_time
                if (update_time.replace(tzinfo=None) + datetime.timedelta(minutes=30)) < \
                        datetime.datetime.utcnow():
                    return render_to_response('register.html', {'phone': phone, 'merchant_name': merchant_name,
                                                                'fault1': 'T'})
                else:
                    newmerchant = Merchant()
                    newmerchant.alin_account = phone
                    password = hashlib.md5(password).hexdigest()
                    newmerchant.password = password
                    newmerchant.name = merchant_name
                    newmerchant.save()
                    request.session['username'] = phone
                    phone_verify.delete()
                    return HttpResponseRedirect("/merchant/operate_new")
            else:
                return render_to_response('register.html', {'phone': phone, 'merchant_name': merchant_name,
                                                            'fault3': 'T'})
        else:
            return render_to_response('register.html')
    else:
        return render_to_response('register.html')


#注册获取验证码
@csrf_exempt
def register_verify(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        merchant_have = Merchant.objects.filter(alin_account=phone)
        if merchant_have.count() > 0:
            return HttpResponse(json.dumps("false"), content_type="application/json")
        req = AlinApi.method.createverfiycode(phone)
        return HttpResponse(json.dumps("true"), content_type="application/json")
    return None



#修改密码
@csrf_exempt
def change_password(request):
    if request.method == 'GET':
        if request.session.get('username'):
            return render_to_response('change_password.html')
        else:
            return HttpResponseRedirect('login_in')
    if request.method == 'POST':
        phone = request.POST.get('phone')
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        new_password_again = request.POST.get('new_password_again')
        if phone and old_password and new_password and new_password_again:
            if not new_password == new_password_again:
                return render_to_response('change_password.html', {'fault2': 'T', 'phone': phone})
            if new_password == old_password:
                return render_to_response('change_password.html', {'fault4': 'T', 'phone': phone})
            if not phone == request.session.get('username'):
                return render_to_response('change_password.html', {'fault3': 'T', 'phone': phone})
            merchant = Merchant.objects.get(alin_account=phone)
            if not merchant.check_password(old_password):
                return render_to_response('change_password.html', {'fault1': 'T', 'phone': phone})
            password = hashlib.md5(new_password).hexdigest()
            merchant.password = password
            merchant.save()
            return render_to_response('change_password.html', {'success': 'T'})
        else:
            return render_to_response('change_password.html')


@csrf_exempt
def change_name(request):
    if request.method == 'GET':
        return render_to_response('change_name.html')
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        new_name = request.POST.get('new_name')
        merchant_phone = request.session['username']
        if phone and password and new_name:
            if not phone == merchant_phone:
                return render_to_response('change_name.html', {'fault1': 'T',
                                                               'phone': phone,
                                                               'new_name': new_name})
            merchant = Merchant.objects.get(alin_account=phone)
            req = merchant.check_password(password)
            if not req:
                return render_to_response('change_name.html', {'fault1': 'T',
                                                               'phone': phone,
                                                               'new_name': new_name})
            merchant.name = new_name
            merchant.save()
            return render_to_response('change_name.html', {'success': 'T', 'new_user_name': new_name})
        else:
            return render_to_response('change_name.html', {'phone': phone, 'new_name': new_name})

#进入未处理订单界面
def operate_new(request):
    if request.method == 'GET':
        if request.session.get('username'):
            try:
                merchant0 = request.session.get('username')
                merchant = Merchant.objects.get(alin_account=merchant0)
                order_detail = DayOrder.objects.order_by('-order_time').filter(merchant=merchant, status=1)
                dish_list = Dish.objects.all
                order_detail = pingtai_name(order_detail)
            except DayOrder.DoesNotExist:
                pass
            return render_to_response('merchant_operate_new.html', {'items': order_detail, 'dishs': dish_list,
                                                                    'user_name': merchant.name})
        else:
            return HttpResponseRedirect("login_in")


#进入已接受订单界面
def operate_get(request):
    if request.method == 'GET':
        if request.session.get('username'):
            try:
                merchant0 = request.session.get('username')
                merchant = Merchant.objects.get(alin_account=merchant0)
                order_detail = DayOrder.objects.order_by('-order_time').filter(merchant=merchant, status=2)
                order_detail = pingtai_name(order_detail)
            except DayOrder.DoesNotExist:
                pass
            return render_to_response('merchant_operate_get.html', {'items': order_detail})
        else:
            return HttpResponseRedirect("login_in")
    return render_to_response('merchant_operate_get.html')


#进入派送订单管理页面
def operate_paisong(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')
    merchant_id = request.session['username']
    merchant = Merchant.objects.get(alin_account=merchant_id)
    express_people = merchant.bind_sender.all()
    orders = DayOrder.objects.order_by('-order_time').filter(merchant=merchant, status=3)
    orders = pingtai_name(orders)
    return render_to_response('merchant_operate_paisong.html', {'orders': orders, 'express_people': express_people})


#进入平台管理页面
def operate_pingtai(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')
    merchant_id = request.session['username']
    merchant = Merchant.objects.get(alin_account=merchant_id)
    items = []
    if merchant.tao_account:
        item = {'name': '1',
                'account': merchant.tao_account}
        items.append(item)
    if merchant.mei_account:
        item = {'name': '3',
                'account': merchant.mei_account}
        items.append(item)
    if merchant.ele_account:
        item = {'name': '2',
                'account': merchant.ele_account}
        items.append(item)

    return render_to_response('merchant_operate_pingtai.html', {'items': items})


#进入删除订单页面
def operate_delete(request):
    if request.method == 'GET':
        if request.session.get('username'):
            try:
                merchant0 = request.session.get('username')
                merchant = Merchant.objects.get(alin_account=merchant0)
                order_detail = DayOrder.objects.order_by('-order_time').filter(merchant=merchant, status=5)
                order_detail = pingtai_name(order_detail)
            except DayOrder.DoesNotExist:
                pass
            return render_to_response('merchant_operate_delete.html', {'items': order_detail})
        else:
            return HttpResponseRedirect("login_in")
    return render_to_response('merchant_operate_delete.html')


#物流人员管理页面
def operate_express_person(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')
    merchant_id = request.session['username']
    merchant = Merchant.objects.get(alin_account=merchant_id)
    express_people = merchant.bind_sender.all()
    return render_to_response('merchant_operate_express_person.html', {'express_people': express_people})


#打印机设置页面
def printer_setting(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')
    return render_to_response('merchant_printer_setting.html')


#加载平台名称
def pingtai_name(orders):
    for item in orders:
        if item.platform == 1:
            item.platform = "淘点点"
        elif item.platform == 3:
            item.platform = "美团"
        elif item.platform == 2:
            item.platform = "饿了么"
        else:
            item.platform = item.platform
    return orders


#打印一个订单
def print_one(request, order):
    try:
        order_detail = DayOrder.objects.get(order_id_alin=order)
        return render_to_response('print.html', {'item': order_detail})
    except DayOrder.DoesNotExist:
        pass


#打印所有订单
def print_all(request):
    try:
        merchant_id = request.session['username']
        merchant = Merchant.objects.get(alin_account=merchant_id)
        order_detail = DayOrder.objects.filter(merchant=merchant, status=1)
        return render_to_response('print_all.html', {'items': order_detail})
    except DayOrder.DoesNotExist:
        pass


#删除平台
def platform_delete(request, name):
    merchant_id = request.session['username']
    merchant = Merchant.objects.get(alin_account=merchant_id)
    if name == '1':
        merchant.tao_account = ''
        merchant.tao_passwd = ''
        merchant.save()
    elif name == '3':
        merchant.mei_account = ''
        merchant.mei_passwd = ''
        merchant.save()
    elif name == '2':
        merchant.ele_account = ''
        merchant.ele_passwd = ''
        merchant.save()
    return HttpResponseRedirect("operate_pingtai")


#进入添加平台页面
def add_platform_page(request):
    return render_to_response('merchant_add_platform.html')


#添加平台
@csrf_exempt
def add_platform(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')
    platform = request.POST.get('platform')
    account = request.POST.get('account')
    password = request.POST.get('password')
    merchant_id = request.session['username']
    merchant = Merchant.objects.get(alin_account=merchant_id)
    if platform == '1' and not merchant.tao_account:
        merchant.tao_account = account
        merchant.tao_passwd = password
        merchant.save()
    elif platform == '3' and not merchant.mei_account:
        merchant.mei_account = account
        merchant.mei_passwd = password
        merchant.save()
    elif platform == '2' and not merchant.ele_account:
        merchant.ele_account = account
        merchant.ele_passwd = password
        merchant.save()
    else:
        return render_to_response('merchant_add_platform.html', {'fault': 'x'})
    return HttpResponseRedirect('operate_pingtai')


#删除物流人员
def delete_sender(request, phone):
    merchant_id = request.session['username']
    merchant = Merchant.objects.get(alin_account=merchant_id)
    sender = Sender.objects.get(phone=phone)
    merchant.bind_sender.remove(sender)
    return HttpResponseRedirect("operate_express_person")


#进入添加物流人员页面
def add_sender_page(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')
    else:
        merchant_id = request.session['username']
        merchant = Merchant.objects.get(alin_account=merchant_id)
        express_people = merchant.bind_sender.all()
        return render_to_response('merchant_add_sender.html', {'express_people': express_people})
