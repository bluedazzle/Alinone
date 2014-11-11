# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponseRedirect
from AlinApi.method import *
from CronOrder.endecy import *
from django.http import HttpResponse, Http404
from AlinApi.models import *
from QRcode.method import *
from django.template import RequestContext
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage

from django.contrib.auth.decorators import login_required
from auth import *
from CronOrder.models import *
import json
import hashlib
import datetime
import time


# Create your views here.
# 登录验证函数
@ensure_csrf_cookie
def login_in(request):
    if 'user_name' in request.POST and request.POST['user_name'] and 'password' in request.POST and request.POST['password']:
        user_name = request.POST['user_name']
        password = request.POST['password']
        try:
            user = Merchant.objects.get(alin_account=user_name)
            if user.check_password(password):
                request.session['username'] = user_name
                merchant = Merchant.objects.get(alin_account=user_name)
                qr_bind = createqr(2, merchant.id)
                request.session['qr_bind'] = qr_bind
                return HttpResponseRedirect("/merchant/operate_new")
            else:
                return render_to_response('login_page.html', {'flag': 1}, context_instance=RequestContext(request))
        except Merchant.DoesNotExist:
            return render_to_response('login_page.html', {'flag': 1}, context_instance=RequestContext(request))
    else:
        return render_to_response('login_page.html', context_instance=RequestContext(request))


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
                                                            'fault3': '2'}, context_instance=RequestContext(request))


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
@ensure_csrf_cookie
def register(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        merchant_name = request.POST.get('merchant_name')
        phone = request.POST.get('phone')
        verify = request.POST.get('verify')
        if password and merchant_name and phone and verify and len(phone) == 11:
            user_test_list = Merchant.objects.filter(alin_account=phone)
            if user_test_list.count() > 0:
                return render_to_response('register.html', {'phone': phone, 'merchant_name': merchant_name,
                                                            'fault2': 'T'}, context_instance=RequestContext(request))
            phone_verify = PhoneVerify.objects.get(phone=str(phone), verify_code=str(verify))
            if phone_verify:
                update_time = phone_verify.update_time
                if (update_time.replace(tzinfo=None) + datetime.timedelta(minutes=30)) < \
                        datetime.datetime.utcnow():
                    return render_to_response('register.html', {'phone': phone, 'merchant_name': merchant_name,
                                                                'fault1': 'T'}, context_instance=RequestContext(request))
                else:
                    newmerchant = Merchant()
                    newmerchant.alin_account = phone
                    password = hashlib.md5(password).hexdigest()
                    newmerchant.password = password
                    newmerchant.name = merchant_name
                    newmerchant.save()
                    request.session['username'] = phone
                    qr_bind = createqr(2, newmerchant.id)
                    request.session['qr_bind'] = qr_bind
                    phone_verify.delete()
                    return HttpResponseRedirect("/merchant/operate_new")
            else:
                return render_to_response('register.html', {'phone': phone, 'merchant_name': merchant_name,
                                                            'fault3': 'T'}, context_instance=RequestContext(request))
        else:
            return render_to_response('register.html', context_instance=RequestContext(request))
    else:
        return render_to_response('register.html', context_instance=RequestContext(request))


#注册获取验证码
def register_verify(request):
    if request.method == 'POST':
        context = {}
        context.update(csrf(request))
        phone = request.POST.get('phone')
        merchant_have = Merchant.objects.filter(alin_account=phone)
        if merchant_have.count() > 0:
            return render_to_response(json.dumps("false"), context_instance=RequestContext(request))
        req = createverfiycode(phone)
        print req
        return render_to_response(json.dumps("true"), content_type="application/json", context_instance=RequestContext(request))
    raise Http404



#修改密码
def change_password(request):
    if request.method == 'GET':
        if request.session.get('username'):
            return render_to_response('change_password.html', context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect('login_in')
    if request.method == 'POST':
        phone = request.POST.get('phone')
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        new_password_again = request.POST.get('new_password_again')
        if phone and old_password and new_password and new_password_again:
            if not new_password == new_password_again:
                return render_to_response('change_password.html', {'fault2': 'T', 'phone': phone}, context_instance=RequestContext(request))
            if new_password == old_password:
                return render_to_response('change_password.html', {'fault4': 'T', 'phone': phone}, context_instance=RequestContext(request))
            if not phone == request.session.get('username'):
                return render_to_response('change_password.html', {'fault3': 'T', 'phone': phone}, context_instance=RequestContext(request))
            merchant = Merchant.objects.get(alin_account=phone)
            if not merchant.check_password(old_password):
                return render_to_response('change_password.html', {'fault1': 'T', 'phone': phone}, context_instance=RequestContext(request))
            password = hashlib.md5(new_password).hexdigest()
            merchant.password = password
            merchant.save()
            return render_to_response('change_password.html', {'success': 'T'}, context_instance=RequestContext(request))
        else:
            return render_to_response('change_password.html', context_instance=RequestContext(request))


def change_name(request):
    if request.method == 'GET':
        return render_to_response('change_name.html', context_instance=RequestContext(request))
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        new_name = request.POST.get('new_name')
        merchant_phone = request.session['username']
        if phone and password and new_name:
            if not phone == merchant_phone:
                return render_to_response('change_name.html', {'fault1': 'T',
                                                               'phone': phone,
                                                               'new_name': new_name}, context_instance=RequestContext(request))
            merchant = Merchant.objects.get(alin_account=phone)
            req = merchant.check_password(password)
            if not req:
                return render_to_response('change_name.html', {'fault1': 'T',
                                                               'phone': phone,
                                                               'new_name': new_name}, context_instance=RequestContext(request))
            merchant.name = new_name
            merchant.save()
            return render_to_response('change_name.html', {'success': 'T', 'new_user_name': new_name}, context_instance=RequestContext(request))
        else:
            return render_to_response('change_name.html', {'phone': phone, 'new_name': new_name}, context_instance=RequestContext(request))


#get orders count
def get_orders_count(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')
    else:
        merchant_id = request.session['username']
        merchant = Merchant.objects.get(alin_account=merchant_id)
        time_now = datetime.datetime.now()
        merchant.last_login = time_now
        merchant.save()
        order_list = DayOrder.objects.filter(merchant=merchant, status=1)
        if order_list.count() == 0:
            count = 'N'
        else:
            count = order_list.count()
        return HttpResponse(json.dumps(count), content_type="application/json")


#进入未处理订单界面
def operate_new(request):
    if request.method == 'GET':
        if request.session.get('username'):
            order_detail = []
            dish_list = []
            try:
                merchant0 = request.session.get('username')
                merchant = Merchant.objects.get(alin_account=merchant0)
                order_detail = DayOrder.objects.order_by('-id').filter(merchant=merchant, status=1)
                request.session['new_order_id'] = order_detail[0].id
                dish_list = Dish.objects.all
                order_detail = pingtai_name(order_detail)
                paginator = Paginator(order_detail, 1)
                try:
                    page_num = request.GET.get('page')
                    order_detail = paginator.page(page_num)
                except PageNotAnInteger:
                    order_detail = paginator.page(1)
                except EmptyPage:
                    order_detail = paginator.page(paginator.num_pages)
                except:
                    pass
            except:
                pass
            return render_to_response('merchant_operate_new.html', {'items': order_detail, 'dishs': dish_list,
                                                                    'user_name': merchant.name},
                                      context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect("login_in")
    else:
        raise Http404


#update orders
def update_new_orders(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')
    else:
        merchant_id = request.session['username']
        merchant = Merchant.objects.get(alin_account=merchant_id)
        order_list = DayOrder.objects.order_by('-id').filter(merchant=merchant, status=1)
        if order_list.count() == 0:
            return HttpResponse(json.dumps('F'), content_type="application/json")
        else:
            if not order_list[0].id == request.session['new_order_id']:
                return HttpResponse(json.dumps('T'), content_type="application/json")
            else:
                return HttpResponse(json.dumps('F'), content_type="application/json")


#进入已接受订单界面
def operate_get(request):
    if request.method == 'GET':
        if request.session.get('username'):
            try:
                merchant0 = request.session.get('username')
                merchant = Merchant.objects.get(alin_account=merchant0)
                order_detail = DayOrder.objects.order_by('-order_time').filter(merchant=merchant, status=2)
                order_detail = pingtai_name(order_detail)
                paginator = Paginator(order_detail, 1)
                try:
                    page_num = request.GET.get('page')
                    order_detail = paginator.page(page_num)
                except PageNotAnInteger:
                    order_detail = paginator.page(1)
                except EmptyPage:
                    order_detail = paginator.page(paginator.num_pages)
                except:
                    pass
            except DayOrder.DoesNotExist:
                pass
            return render_to_response('merchant_operate_get.html', {'items': order_detail}, context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect("login_in")
    return render_to_response('merchant_operate_get.html', context_instance=RequestContext(request))


#进入派送订单管理页面
def operate_paisong(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')
    merchant_id = request.session['username']
    merchant = Merchant.objects.get(alin_account=merchant_id)
    express_people = merchant.bind_sender.all()
    orders = DayOrder.objects.order_by('-order_time').filter(merchant=merchant, status=3)
    orders = pingtai_name(orders)
    return render_to_response('merchant_operate_paisong.html', {'orders': orders, 'express_people': express_people}, context_instance=RequestContext(request))


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

    return render_to_response('merchant_operate_pingtai.html', {'items': items}, context_instance=RequestContext(request))


#进入删除订单页面
def operate_delete(request):
    if request.method == 'GET':
        if request.session.get('username'):
            try:
                merchant0 = request.session.get('username')
                merchant = Merchant.objects.get(alin_account=merchant0)
                order_detail = DayOrder.objects.order_by('-order_time').filter(merchant=merchant, status=5)
                order_detail = pingtai_name(order_detail)
                paginator = Paginator(order_detail, 1)
                try:
                    page_num = request.GET.get('page')
                    order_detail = paginator.page(page_num)
                except PageNotAnInteger:
                    order_detail = paginator.page(1)
                except EmptyPage:
                    order_detail = paginator.page(paginator.num_pages)
                except:
                    pass
            except DayOrder.DoesNotExist:
                pass
            return render_to_response('merchant_operate_delete.html', {'items': order_detail}, context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect("login_in")
    return render_to_response('merchant_operate_delete.html', context_instance=RequestContext(request))


#物流人员管理页面
def operate_express_person(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')
    merchant_id = request.session['username']
    merchant = Merchant.objects.get(alin_account=merchant_id)
    express_people = merchant.bind_sender.all()
    return render_to_response('merchant_operate_express_person.html', {'express_people': express_people}, context_instance=RequestContext(request))


#打印机设置页面
def printer_setting(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')
    return render_to_response('merchant_printer_setting.html', context_instance=RequestContext(request))


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
        return render_to_response('print.html', {'item': order_detail}, context_instance=RequestContext(request))
    except DayOrder.DoesNotExist:
        pass


#打印所有订单
def print_all(request):
    try:
        merchant_id = request.session['username']
        merchant = Merchant.objects.get(alin_account=merchant_id)
        order_detail = DayOrder.objects.filter(merchant=merchant, status=1)
        return render_to_response('print_all.html', {'items': order_detail}, context_instance=RequestContext(request))
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
    return render_to_response('merchant_add_platform.html', context_instance=RequestContext(request))


#添加平台
def add_platform(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')
    platform = request.POST.get('platform')
    account = request.POST.get('account')
    password = str(request.POST.get('password'))
    password = Encrypt(password)
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
        return render_to_response('merchant_add_platform.html', {'fault': 'x'}, context_instance=RequestContext(request))
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
        request.session['sender_count'] = express_people.count()
        filename = request.session['qr_bind']
        return render_to_response('merchant_add_sender.html', {'express_people': express_people, 'filename': filename})


#get sender change
def get_sender_change(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')
    else:
        merchant_id = request.session['username']
        merchant = Merchant.objects.get(alin_account=merchant_id)
        express_people = merchant.bind_sender.all()
        if request.session.get('sender_count'):
            if request.session['sender_count'] == express_people.count():
                return HttpResponse(json.dumps('F'), content_type="application/json")
            else:
                return HttpResponse(json.dumps('T'), content_type="application/json")
        else:
            return HttpResponse(json.dumps('T'), content_type="application/json")