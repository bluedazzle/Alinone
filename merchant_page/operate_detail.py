# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from auth import *
from CronOrder.models import *
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


def jieshouone(request, order):
    order_detail = DayOrder.objects.get(order_id_alin=order)
    order_detail.status = 2
    order_detail.save()
    return HttpResponseRedirect("operate_new")


def jujueone(request, order):
    order_detail = DayOrder.objects.get(order_id_alin=order)
    order_detail.status = 5
    order_detail.save()
    return HttpResponseRedirect("operate_new")


def jieshouall(request):
    merchant0 = request.session.get('username')
    merchant = Merchant.objects.get(alin_account=merchant0)
    order_detail = DayOrder.objects.filter(merchant=merchant, status=1)
    for item in order_detail:
        item.status = 2
        item.save()
    return HttpResponseRedirect("operate_new")


def jujueall(request):
    merchant0 = request.session.get('username')
    merchant = Merchant.objects.get(alin_account=merchant0)
    order_detail = DayOrder.objects.filter(merchant=merchant, status=1)
    for item in order_detail:
        item.status = 5
        item.save()
    return HttpResponseRedirect("operate_new")
