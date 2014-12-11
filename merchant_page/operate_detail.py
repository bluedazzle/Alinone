# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from auth import *
from CronOrder.models import *
from merchant_page.views import *
from AlinApi.views import isactive
import json
import hashlib
import urllib


# def fuwei(request):
#     merchant0 = request.session.get('username')
#     merchant = Merchant.objects.get(alin_account=merchant0)
#     order_detail = DayOrder.objects.filter(merchant=merchant)
#     for item in order_detail:
#         item.status = 1
#         item.save()
#     return HttpResponseRedirect("operate_new")

def netSpiderStatus(req):
    merchant0 = request.session.get('username')
    merchant = Merchant.objects.get(alin_account=merchant0)
    mystatus = merchant.netspider_time.replace(tzinfo = None)
    return isactive(mystatus, 30)


def jieshouone(request, order):
    global alo
    if not request.session.get('username'):
        return HttpResponse(json.dumps('N'), content_type='application/json')
    merchant0 = request.session.get('username')
    currentusr = Merchant.objects.get(alin_account=merchant0)
    order_detail = DayOrder.objects.get(order_id_alin=order)
    order_detail.status = 2
    orderstr = str(order_detail.order_id_old) + ',' + str(order_detail.platform)
    res = alo.ensure_order(str(currentusr.id), orderstr)
    if res:
        order_detail.save()
    return HttpResponse(json.dumps('T'), content_type='application/json')


def jujueone(request, order):
    if not request.session.get('username'):
        return HttpResponse(json.dumps('N'), content_type='application/json')
    merchant0 = request.session.get('username')
    currentusr = Merchant.objects.get(alin_account=merchant0)
    order_detail = DayOrder.objects.get(order_id_alin=order)
    orderstr = str(order_detail.order_id_old) + ',' + str(order_detail.platform)
    res = alo.refuse_order(str(currentusr.id), orderstr)
    if res:
        order_detail.status = 5
        order_detail.save()
    return HttpResponse(json.dumps('T'), content_type='application/json')


def jieshouall(request):
    if not request.session.get('username'):
        return HttpResponse(json.dumps('N'), content_type='application/json')
    merchant0 = request.session.get('username')
    merchant = Merchant.objects.get(alin_account=merchant0)
    order_detail = DayOrder.objects.filter(merchant=merchant, status=1)
    for item in order_detail:
        orderstr = str(item.order_id_old) + ',' + str(item.platform)
        res = alo.ensure_order(str(merchant.id), orderstr)
        if res:
            item.status = 2
            item.save()
    return HttpResponse(json.dumps('T'), content_type='application/json')


def jujueall(request):
    if not request.session.get('username'):
        return HttpResponse(json.dumps('N'), content_type='application/json')
    merchant0 = request.session.get('username')
    merchant = Merchant.objects.get(alin_account=merchant0)
    order_detail = DayOrder.objects.filter(merchant=merchant, status=1)
    for item in order_detail:
        orderstr = str(item.order_id_old) + ',' + str(item.platform)
        res = alo.refuse_order(str(merchant.id), orderstr)
        if res:
            item.status = 5
            item.save()
    return HttpResponse(json.dumps('T'), content_type='application/json')


def finishall(request):
    if not request.session.get('username'):
        return HttpResponse(json.dumps('N'), content_type='application/json')
    merchant0 = request.session.get('username')
    merchant = Merchant.objects.get(alin_account=merchant0)
    order_detail = DayOrder.objects.filter(merchant=merchant, status=2)
    for item in order_detail:
        item.status = 4
        item.save()
    return HttpResponse(json.dumps('T'), content_type='application/json')


def finishone(request):
    if not request.session.get('username'):
        return HttpResponse(json.dumps('N'), content_type='application/json')
    order_id_alin = request.GET.get('order')
    order_detail = DayOrder.objects.get(order_id_alin=order_id_alin)
    order_detail.status = 4
    order_detail.save()
    return HttpResponse(json.dumps('T'), content_type='application/json')


def add_order(request):
    if request.method == 'GET':
        if not request.session.get('username'):
            return HttpResponseRedirect('login_in')
        money = request.GET.get('money')
        phone = request.GET.get('phone')
        address = request.GET.get('address')
        platform = request.GET.get('platform')
        ifcharge = str(request.GET.get('ifcharge'))
        pay = False
        if money and phone and address and platform:
            try:
                merchant = Merchant.objects.get(alin_account=request.session['username'])
                autoid = int(DayOrder.objects.filter(platform=platform, merchant=merchant).count()) + 1
                if ifcharge == '1':
                    pay = True
                new_order = DayOrder()
                newid = createAlinOrderNum(str(platform), merchant.id, autoid)
                new_order.order_id_alin = newid
                new_order.qr_path = createqr(1, newid)
                new_order.order_id_old = str(autoid)
                new_order.phone = phone
                new_order.address = address
                new_order.platform = platform
                new_order.status = 2
                new_order.pay = pay
                new_order.real_price = money
                new_order.merchant = merchant
                new_order.origin_price = money
                new_order.order_time = datetime.datetime.now()
                new_order.send_time = datetime.datetime.now()
                new_order.save()
                return HttpResponse(json.dumps('T'), content_type='application/json')
            except:
                return HttpResponse(json.dumps('F'), content_type='application/json')
        else:
            return HttpResponse(json.dumps('F'), content_type='application/json')
    else:
        return HttpResponseRedirect('operate_new')

