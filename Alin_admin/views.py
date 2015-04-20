# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
from AlinLog.models import AccountLog
from models import *
from merchant_page.models import *
from CronOrder.Aaps import *
from CronOrder.ALO import *
import json
import time
import simplejson
import hashlib
import datetime


def login(request):
    if request.method == 'GET':
        return render_to_response('alin_admin/login.html',
                                  context_instance=RequestContext(request))
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.check_valid():
            request.session['alin_admin'] = login_form.cleaned_data['username']
            return HttpResponseRedirect('admin_host')
        else:
            return render_to_response('alin_admin/login.html',
                                      {'login_fault': True},
                                      context_instance=RequestContext(request))


def if_login(request):
    if request.session.get('alin_admin'):
        return True
    else:
        return False


def alin_admin_host(request):
    if not if_login(request):
        return HttpResponseRedirect('admin_login')
    if request.method == 'GET':
        return render_to_response('alin_admin/admin_host.html')


def count(request):
    if not if_login(request):
        return HttpResponse(json.dumps('F'))
    if request.method == 'GET':
        content = dict()

        user_online = Merchant.objects.filter(is_online=True)
        content['user_online_number'] = user_online.count()

        orders_all = DayOrder.objects.all()
        content['order_all_number'] = orders_all.count()

        today_date = datetime.date.today()
        one_day = datetime.timedelta(days=1)
        today = datetime.datetime.combine(today_date, datetime.time(0, 0, 0))
        tomorrow = today + one_day
        order_today = DayOrder.objects.filter(order_time__gte=today,
                                              order_time__lte=tomorrow)
        content['order_today_number'] = order_today.count()

        return HttpResponse(json.dumps(content))


def verify_merchant(request):
    if not if_login(request):
        return HttpResponseRedirect('admin_login')
    if request.method == 'GET':
        merchants = Merchant.objects.filter(verify=False)
        paginator = Paginator(merchants, 20)
        try:
            page_num = request.GET.get('page')
            merchants = paginator.page(page_num)
        except PageNotAnInteger:
            merchants = paginator.page(1)
        except EmptyPage:
            merchants = paginator.page(paginator.num_pages)
        except:
            pass
        return render_to_response('alin_admin/merchant_verify.html',
                                  {'merchants': merchants},
                                  context_instance=RequestContext(request))


def pass_merchant(request):
    if not if_login(request):
        return HttpResponseRedirect('admin_login')
    if request.method == 'POST':
        merchant_id = request.POST.get('merchant_id')
        if not merchant_id:
            raise Http404
        merchant = Merchant.objects.get(id=merchant_id)
        try:
            merchant.verify = True
            merchant.save()
        except:
            raise Http404
        return HttpResponse('T')


def reject_merchant(request):
    if not if_login(request):
        return HttpResponseRedirect('admin_login')
    if request.method == 'POST':
        merchant_id = request.POST.get('merchant_id')
        if not merchant_id:
            raise Http404
        merchant = Merchant.objects.get(id=merchant_id)
        try:
            merchant.delete()
        except:
            raise Http404
        return HttpResponse('T')


def merchant_list(request):
    if not if_login(request):
        return HttpResponseRedirect('admin_login')
    if request.method == 'GET':
        merchants = Merchant.objects.order_by('-id').all()
        paginator = Paginator(merchants, 20)
        try:
            page_num = request.GET.get('page')
            merchants = paginator.page(page_num)
        except PageNotAnInteger:
            merchants = paginator.page(1)
        except EmptyPage:
            merchants = paginator.page(paginator.num_pages)
        except:
            pass
        return render_to_response('alin_admin/merchant_list.html',
                                  {'merchants': merchants},
                                  context_instance=RequestContext(request))


def manage_log(request):
    if not if_login(request):
        return HttpResponseRedirect('admin_login')
    if request.method == 'GET':
        return render_to_response('alin_admin/log_manage.html',
                                  context_instance=RequestContext(request))


def account_log(request):
    if not if_login(request):
        return HttpResponseRedirect('admin_login')
    if request.method == 'GET':
        start_time = request.GET.get('start_time')
        end_time = request.GET.get('end_time')
        if start_time and end_time:
            start_datetime = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            end_datetime = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
            account_logs = AccountLog.objects.order_by('-id').filter(log_time__lte=end_datetime,
                                                                     log_time__gte=start_datetime)
        else:
            start_time = ''
            end_time = ''
            account_logs = AccountLog.objects.order_by('-id').all()

        paginator = Paginator(account_logs, 20)
        try:
            page_num = request.GET.get('page')
            account_logs = paginator.page(page_num)
        except PageNotAnInteger:
            account_logs = paginator.page(1)
        except EmptyPage:
            account_logs = paginator.page(paginator.num_pages)
        except:
            pass
        return render_to_response('alin_admin/log/account_log.html',
                                  {'account_logs': account_logs,
                                   'start_time': start_time,
                                   'end_time': end_time},
                                  context_instance=RequestContext(request))


def cron_log(request):
    if not if_login(request):
        return HttpResponseRedirect('admin_login')
    if request.method == 'GET':
        cron_logs = CronLog.objects.order_by('-id').all()
        return render_to_response('alin_admin/log/cron_log.html',
                                  {'cron_logs': cron_logs},
                                  context_instance=RequestContext(request))


def pro_run_time_log(request):
    if not if_login(request):
        return HttpResponseRedirect('admin_login')
    if request.method == 'GET':
        pro_run_time_logs = ProRunTimeLog.objects.order_by('-id').all()
        return render_to_response('alin_admin/log/pro_run_time_log.html',
                                  {'pro_run_time_logs': pro_run_time_logs},
                                  context_instance=RequestContext(request))


def run_time_log(request):
    if not if_login(request):
        return HttpResponseRedirect('admin_login')
    if request.method == 'GET':
        run_time_logs = RunTimeLog.objects.order_by('-id').all()
        return render_to_response('alin_admin/log/run_time_log.html',
                                  {'run_time_logs': run_time_logs},
                                  context_instance=RequestContext(request))


def seach_log(request):
    if not if_login(request):
        return HttpResponseRedirect('admin_login')
    if request.method == 'GET':
        seach_logs = SeachLog.objects.order_by('-id').all()
        return render_to_response('alin_admin/log/seach_log.html',
                                  {'seach_logs': seach_logs},
                                  context_instance=RequestContext(request))


def logout(request):
    if not if_login(request):
        return HttpResponseRedirect('admin_login')
    if request.method == 'GET':
        del request.session['alin_admin']
        return HttpResponseRedirect('admin_login')




def create_order(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        for i in range(0, 100):
            new_order = DayOrder()
            order_id = str(int(time.time())) + id + str(i)
            new_order.order_id_alin = order_id
            new_order.order_id_old = order_id
            new_order.order_time = datetime.datetime.utcnow()
            new_order.send_time = datetime.datetime.utcnow()
            new_order.phone = str(random.randint(11111111111, 99999999999))
            new_order.pay = True
            new_order.address = "asldfkjalsdkfj"
            new_order.platform = random.randint(1, 3)
            new_order.origin_price = float(random.randint(10, 20))
            new_order.real_price = new_order.origin_price - 5.0
            new_order.status = 1
            new_order.merchant = Merchant.objects.all().first()
            new_order.save()

        return HttpResponse('OK')