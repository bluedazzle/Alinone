# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from auth import *
from CronOrder.models import *
import json
import hashlib
import urllib


# Create your views here.
@csrf_exempt
def login_in(request):
    if 'user_name' in request.POST and request.POST['user_name'] and 'password' in request.POST and request.POST['password']:
        user_name = request.POST['user_name']
        password = request.POST['password']
        try:
            user = Merchant.objects.get(alin_account=user_name)
            if user.check_password(password):
                request.session['username'] = user_name
                return HttpResponseRedirect("operate_new")
            else:
                return render_to_response('login_fault.html')
        except Merchant.DoesNotExist:
            return render_to_response('login_fault.html')
    else:
        return render_to_response('login_page.html')


def login_out(request):
    del request.session['username']
    return HttpResponseRedirect("login_in")


@csrf_exempt
def register(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        merchant_name = request.POST.get('merchant_name')
        phone = request.POST.get('phone')
        if password and merchant_name and phone:
            newmerchant = Merchant()
            newmerchant.alin_account = phone
            password = hashlib.md5(password).hexdigest()
            newmerchant.password = password
            newmerchant.name = merchant_name
            newmerchant.save()
            return HttpResponseRedirect("operate_new")
        else:
            return render_to_response('register.html')
    else:
        return render_to_response('register.html')


# def login_ver(request):
#     if 'user_name' in request.GET and request.GET['user_name'] and 'password' in request.GET and request.GET['password']:
#         user_name = request.GET['user_name']
#         password = request.GET['password']
#         return render_to_response('merchant_operate_new.html')
#     else:
#         return None


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
            return render_to_response('merchant_operate_new.html', {'items': order_detail, 'dishs': dish_list})
        else:
            return HttpResponseRedirect("login_in")


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


def operate_paisong(request):
    merchant_id = request.session['username']
    merchant = Merchant.objects.get(alin_account=merchant_id)
    express_people = merchant.bind_sender.all()
    orders = DayOrder.objects.order_by('-order_time').filter(merchant=merchant, status=3)
    orders = pingtai_name(orders)
    return render_to_response('merchant_operate_paisong.html', {'orders': orders, 'express_people': express_people})


def operate_pingtai(request):
    merchant_id = request.session['username']
    merchant = Merchant.objects.get(alin_account=merchant_id)
    items = []
    if merchant.tao_account:
        item = {'name': '1',
                'account': merchant.tao_account}
        items.append(item)
    if merchant.mei_account:
        item = {'name': '2',
                'account': merchant.mei_account}
        items.append(item)
    if merchant.ele_account:
        item = {'name': '3',
                'account': merchant.ele_account}
        items.append(item)

    return render_to_response('merchant_operate_pingtai.html', {'items': items})


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


def operate_express_person(request):
    merchant_id = request.session['username']
    merchant = Merchant.objects.get(alin_account=merchant_id)
    express_people = merchant.bind_sender.all()
    return render_to_response('merchant_operate_express_person.html', {'express_people': express_people})


def printer_setting(request):
    return render_to_response('merchant_printer_setting.html')


def pingtai_name(orders):
    for item in orders:
        if item.platform == 1:
            item.platform = "淘点点"
        elif item.platform == 2:
            item.platform = "美团"
        elif item.platform == 3:
            item.platform = "饿了么"
        else:
            item.platform = item.platform
    return orders


def print_one(request, order):
    try:
        order_detail = DayOrder.objects.get(order_id_alin=order)
        return render_to_response('print.html', {'item': order_detail})
    except DayOrder.DoesNotExist:
        pass


def print_all(request):
    try:
        merchant_id = request.session['username']
        merchant = Merchant.objects.get(alin_account=merchant_id)
        order_detail = DayOrder.objects.filter(merchant=merchant, status=1)
        return render_to_response('print_all.html', {'items': order_detail})
    except DayOrder.DoesNotExist:
        pass


def platform_delete(request, name):
    merchant_id = request.session['username']
    merchant = Merchant.objects.get(alin_account=merchant_id)
    if name == '1':
        merchant.tao_account = ''
        merchant.tao_passwd = ''
        merchant.save()
    elif name == '2':
        merchant.mei_account = ''
        merchant.mei_passwd = ''
        merchant.save()
    elif name == '3':
        merchant.ele_account = ''
        merchant.ele_passwd = ''
        merchant.save()
    return HttpResponseRedirect("operate_pingtai")


def add_platform_page(request):
    return render_to_response('merchant_add_platform.html')


@csrf_exempt
def add_platform(request):
    platform = request.POST.get('platform')
    account = request.POST.get('account')
    password = request.POST.get('password')
    merchant_id = request.session['username']
    merchant = Merchant.objects.get(alin_account=merchant_id)
    if platform == '1' and not merchant.tao_account:
        merchant.tao_account = account
        merchant.tao_passwd = password
        merchant.save()
    elif platform == '2' and not merchant.mei_account:
        merchant.mei_account = account
        merchant.mei_passwd = password
        merchant.save()
    elif platform == '3' and not merchant.ele_account:
        merchant.ele_account = account
        merchant.ele_passwd = password
        merchant.save()
    else:
        return render_to_response('merchant_add_platform.html', {'fault': 'x'})
    return HttpResponseRedirect('operate_pingtai')


def delete_sender(request, phone):
    merchant_id = request.session['username']
    merchant = Merchant.objects.get(alin_account=merchant_id)
    sender = Sender.objects.get(phone=phone)
    merchant.bind_sender.remove(sender)
    return HttpResponseRedirect("operate_express_person")


def add_sender_page(request):
    return render_to_response('merchant_add_sender.html')
