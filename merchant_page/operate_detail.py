# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from auth import *
from CronOrder.models import *
from AlinApi.views import isactive
import json
import hashlib
import urllib


def fuwei(request):
    merchant0 = request.session.get('username')
    merchant = Merchant.objects.get(alin_account=merchant0)
    order_detail = DayOrder.objects.filter(merchant=merchant)
    for item in order_detail:
        item.status = 1
        item.save()
    return HttpResponseRedirect("operate_new")

def netSpiderStatus(req):
    merchant0 = request.session.get('username')
    merchant = Merchant.objects.get(alin_account=merchant0)
    mystatus = merchant.netspider_time.replace(tzinfo = None)
    return isactive(mystatus, 30)


def jieshouone(request, order):
    if not request.session.get('username'):
        return HttpResponse(json.dumps('N'), content_type='application/json')
    order_detail = DayOrder.objects.get(order_id_alin=order)
    order_detail.status = 2
    order_detail.save()
    return HttpResponse(json.dumps('T'), content_type='application/json')


def jujueone(request, order):
    if not request.session.get('username'):
        return HttpResponse(json.dumps('N'), content_type='application/json')
    order_detail = DayOrder.objects.get(order_id_alin=order)
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
        item.status = 2
        item.save()
    return HttpResponse(json.dumps('T'), content_type='application/json')


def jujueall(request):
    if not request.session.get('username'):
        return HttpResponse(json.dumps('N'), content_type='application/json')
    merchant0 = request.session.get('username')
    merchant = Merchant.objects.get(alin_account=merchant0)
    order_detail = DayOrder.objects.filter(merchant=merchant)
    for item in order_detail:
        item.status = 5
        item.save()
    return HttpResponse(json.dumps('T'), content_type='application/json')


def finishall(request):
    if not request.session.get('username'):
        return HttpResponse(json.dumps('N'), content_type='application/json')
    merchant0 = request.session.get('username')
    merchant = Merchant.objects.get(alin_account=merchant0)
    order_detail = DayOrder.objects.filter(merchant=merchant)
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
