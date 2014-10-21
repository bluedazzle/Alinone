# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from auth import *
from CronOrder.models import *
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
                order_detail = DayOrder.objects.filter(merchant=merchant, status=1)
                for item in order_detail:
                    if item.platform == 1:
                        item.platform = "淘点点"
                    elif item.platform == 2:
                        item.platform = "美团"
                    elif item.platform == 3:
                        item.platform = "饿了么"
                    else:
                        item.platform = item.platform
            except DayOrder.DoesNotExist:
                pass
            return render_to_response('merchant_operate_new.html', {'items': order_detail})
        else:
            return HttpResponseRedirect("login_in")


def operate_get(request):
    if request.method == 'GET':
        if request.session.get('username'):
            try:
                merchant0 = request.session.get('username')
                merchant = Merchant.objects.get(alin_account=merchant0)
                order_detail = DayOrder.objects.filter(merchant=merchant, status=2)
                for item in order_detail:

                    if item.platform == 1:
                        item.platform = "淘点点"
                    elif item.platform == 2:
                        item.platform = "美团"
                    elif item.platform == 3:
                        item.platform = "饿了么"
                    else:
                        item.platform = item.platform
            except DayOrder.DoesNotExist:
                pass
            return render_to_response('merchant_operate_get.html', {'items': order_detail})
        else:
            return HttpResponseRedirect("login_in")
    return render_to_response('merchant_operate_get.html')


def operate_paisong(request):
    return render_to_response('merchant_operate_paisong.html')


def operate_pingtai(request):
    return render_to_response('merchant_operate_pingtai.html')


def operate_delete(request):
    if request.method == 'GET':
        if request.session.get('username'):
            try:
                merchant0 = request.session.get('username')
                merchant = Merchant.objects.get(alin_account=merchant0)
                order_detail = DayOrder.objects.filter(merchant=merchant, status=5)
                for item in order_detail:

                    if item.platform == 1:
                        item.platform = "淘点点"
                    elif item.platform == 2:
                        item.platform = "美团"
                    elif item.platform == 3:
                        item.platform = "饿了么"
                    else:
                        item.platform = item.platform
            except DayOrder.DoesNotExist:
                pass
            return render_to_response('merchant_operate_delete.html', {'items': order_detail})
        else:
            return HttpResponseRedirect("login_in")
    return render_to_response('merchant_operate_delete.html')


def operate_express_person(request):
    return render_to_response('merchant_operate_express_person.html')