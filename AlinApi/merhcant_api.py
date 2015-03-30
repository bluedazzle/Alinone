# -*- coding: utf-8 -*-
from CronOrder.models import *
from AlinApi.models import PhoneVerify
from QRcode.method import *
from django.views.decorators.csrf import csrf_exempt
from AlinApi.method import *
from django.http import HttpResponse, Http404
from django.utils import timezone
from CronOrder.ALO import *
import simplejson
import sys
import copy


@csrf_exempt
def send_verify(req):
    if req.method == 'POST':
        jsonres = simplejson.loads(req.body)
        phone = jsonres['phone']
        verify_res = createverfiycode(phone)
        verify_res = simplejson.loads(verify_res)
        if verify_res['success'] is True:
            try:
                verify = PhoneVerify.objects.get(phone=phone)
                verify.verify_code = verify_res['verify_code']
                verify.save()
            except Exception:
                newverify = PhoneVerify(phone=phone, verify_code=verify_res['verify_code'])
                newverify.save()
            return HttpResponse(encodejson(1, verify_res), content_type='application/json')
        else:
            return HttpResponse(encodejson(2, {}), content_type='application/json')
    else:

        raise Http404


@csrf_exempt
def register(req):
    body={}
    if req.method == 'POST':
        resjson = simplejson.loads(req.body)
        phone = resjson['phone']
        verify = resjson['verify_code']
        passwd = resjson['password']
        mer_name = resjson['merchant_name']
        me_list = Merchant.objects.filter(alin_account=phone)
        if me_list.exists():
            body['msg'] = 'account aleady exist'
            return HttpResponse(encodejson(6, body), content_type="application/json")
        if not verify_code(phone, verify):
            body['msg'] = 'verify code does not exist'
            return HttpResponse(encodejson(7, body), content_type='application/json')
        hashpass = hashlib.md5(passwd).hexdigest()
        mytoken = createtoken()
        newmerchant = Merchant(alin_account=phone,
                               password=hashpass,
                               active_time=datetime.datetime.now(),
                               name=mer_name,
                               private_token=mytoken)
        newmerchant.save()
        body['msg'] = 'register success, wait for auth'
        return HttpResponse(encodejson(0, body), content_type='application/json')
    else:
        raise Http404



@csrf_exempt
def login(req):
    body={}
    if req.method == 'POST':
        resjson = simplejson.loads(req.body)
        username = resjson['username']
        passwd = resjson['password']
        me_list = Merchant.objects.filter(alin_account=username)
        if not me_list.exists():
            body['msg'] = 'account not exist'
            return HttpResponse(encodejson(6, body), content_type='application/json')
        curuser = me_list[0]
        if not curuser.verify:
            body['msg'] = 'wait for auth'
            return HttpResponse(encodejson(0, body), content_type='application/json')
        if not curuser.check_password(passwd):
            body['msg'] = 'account or password not correct'
            return HttpResponse(encodejson(4, body), content_type='application/json')
        newtoken = createtoken()
        curuser.private_token = newtoken
        curuser.save()
        body['private_token'] = newtoken
        return HttpResponse(encodejson(1, body), content_type='application/json')
    else:
        raise Http404


@csrf_exempt
def logout(req):
    body={}
    if req.method == 'POST':
        resjson = simplejson.loads(req.body)
        username = resjson['username']
        token = resjson['private_token']
        if not if_legal(username, token):
            body['msg'] = 'auth failed'
            return HttpResponse(encodejson(13, body), content_type='application/json')
        me = Merchant.objects.get(alin_account=username)
        me.private_token = ''
        me.save()
        return HttpResponse(encodejson(1, body), content_type='application/json')
    else:
        raise Http404


@csrf_exempt
def get_new_order(req):
    body={}
    if not req.method == 'POST':
        raise Http404
    resjson = simplejson.loads(req.body)
    username = resjson['username']
    token = resjson['private_token']
    if not if_legal(username, token):
        body['msg'] = 'auth failed'
        return HttpResponse(encodejson(13, body), content_type='application/json')
    curuser = Merchant.objects.get(alin_account=username)
    new_order_list = DayOrder.objects.filter(status=1, merchant=curuser)
    alo = Alo()
    alo.cronOrder(str(curuser.id))
    if new_order_list.exists():
        # order_list = []
        # for itm in new_order_list:
        #     order = {}
        #     order['order_id'] = itm.order_id_alin
        #     order_list.append(copy.copy(order))
        body['have_new'] = True
        # body['order_list'] = order_list
        body['count'] = new_order_list.count()
        body['msg'] = 'new orders!'
        return HttpResponse(encodejson(1, body), content_type='application/json')
    else:
        body['have_new'] = False
        body['msg'] = 'no new order'
        return HttpResponse(encodejson(1, body), content_type='application/json')



@csrf_exempt
def get_pending_order_detail(req):
    body={}
    if not req.method == 'POST':
        raise Http404
    resjson = simplejson.loads(req.body)
    username = resjson['username']
    token = resjson['private_token']
    if not if_legal(username, token):
        body['msg'] = 'auth failed'
        return HttpResponse(encodejson(13, body), content_type='application/json')
    curuser = Merchant.objects.get(alin_account=username)
    new_order_list = DayOrder.objects.filter(status=1, merchant=curuser)
    order_list = []
    for item in new_order_list:
        order = {}
        order['alin_id'] = item.order_id_alin
        order['old_id'] = item.order_id_old
        order['order_time'] = datetime_to_string(item.order_time)
        order['send_time'] = datetime_to_string(item.send_time)
        order['phone'] = item.phone
        order['pay'] = item.pay
        order['address'] = item.address
        order['platform'] = item.platform
        order['real_price'] = item.real_price
        order['note'] = item.note
        order['plat_number'] = item.plat_num
        order['day_number'] = item.day_num
        dish_list = Dish.objects.filter(order=item)
        dishs = []
        for itm in dish_list:
            dish = {}
            dish['dish_name'] = itm.dish_name
            dish['dish_count'] = itm.dish_count
            dish['dish_price'] = itm.dish_price
            dishs.append(copy.copy(dish))
        order['dish_list'] = dishs
        order_list.append(copy.copy(order))
    body['msg'] = 'pending orders get success'
    body['order_list'] = order_list
    return HttpResponse(encodejson(1, body), content_type='application/json')


@csrf_exempt
def ensure_order(req):
    body={}
    if not req.method == 'POST':
        raise Http404
    resjson = simplejson.loads(req.body)
    username = resjson['username']
    order_id = resjson['order_id']
    token = resjson['private_token']
    if not if_legal(username, token):
        body['msg'] = 'auth failed'
        return HttpResponse(encodejson(13, body), content_type='application/json')
    order_list = DayOrder.objects.filter(order_id_alin=order_id)
    if order_list.exists():
        curuser = Merchant.objects.get(alin_account=username)
        order = order_list[0]
        platform = order.platform
        orderstr = str(order.order_id_old) + ',' + str(platform)
        print 'hhh'
        print orderstr
        alo = Alo()
        res = alo.ensure_order(curuser.id, orderstr)
        if res:
            order.status = 2
            order.save()
            body['msg'] = 'accept order success'
            return HttpResponse(encodejson(1, body), content_type='application/json')
        else:
            body['msg'] = 'accept order failed'
            return HttpResponse(encodejson(2, body), content_type='application/json')
    else:
        body['msg'] = 'invalid order id'
        return HttpResponse(encodejson(7, body), content_type='appliation/json')



@csrf_exempt
def refuse_order(req):
    body={}
    if not req.method == 'POST':
        raise Http404
    resjson = simplejson.loads(req.body)
    username = resjson['username']
    order_id = resjson['order_id']
    token = resjson['private_token']
    if not if_legal(username, token):
        body['msg'] = 'auth failed'
        return HttpResponse(encodejson(13, body), content_type='application/json')
    order_list = DayOrder.objects.filter(order_id_alin=order_id)
    if order_list.exists():
        curuser = Merchant.objects.get(alin_account=username)
        order = order_list[0]
        platform = order.platform
        orderstr = str(order.order_id_old) + ',' + str(platform)
        alo = Alo()
        res = alo.refuse_order(curuser.id, orderstr)
        if res:
            order.status = 5
            order.save()
            body['msg'] = 'refuse order success'
            return HttpResponse(encodejson(1, body), content_type='application/json')
        else:
            body['msg'] = 'refuse order failed'
            return HttpResponse(encodejson(2, body), content_type='application/json')
    else:
        body['msg'] = 'invalid order id'
        return HttpResponse(encodejson(7, body), content_type='appliation/json')



@csrf_exempt
def create_new_order(req):
    body = {}
    if not req.method == 'POST':
        raise Http404
    resjson = simplejson.loads(req.body)
    username = resjson['username']
    token = resjson['private_token']
    if not if_legal(username, token):
        body['msg'] = 'auth failed'
        return HttpResponse(encodejson(13, body), content_type='application/json')
    curuser = Merchant.objects.get(alin_account=username)
    price = resjson['price']
    phone = resjson['phone']
    address = resjson['address']
    platform = resjson['platform']
    pay = resjson['if_pay']
    autoid = int(DayOrder.objects.filter(platform=platform, merchant=curuser).count()) + 1
    new_id = createAlinOrderNum(str(platform), curuser.id, autoid)
    qr_path = createqr(1, new_id)
    new_order = DayOrder(
        order_id_alin=new_id,
        order_id_old=str(autoid),
        phone=phone,
        address=address,
        platform=platform,
        status=2,
        pay=pay,
        real_price=price,
        origin_price=price,
        merchant=curuser,
        note='',
        plat_num='',
        order_time=datetime.datetime.now(),
        send_time=datetime.datetime.now(),
        qr_path=qr_path
    )
    new_order.save()
    body['msg'] = 'create new order success'
    return HttpResponse(encodejson(1, body), content_type='application/json')






def verify_code(phone, verify_code):
        verify_list = PhoneVerify.objects.filter(phone=phone, verify_code=str(verify_code))
        if verify_list.count() > 0:
            verify = verify_list[0]
            verify.delete()
            return True
        else:
            return False


def if_legal(username, private_token):
    print username
    print private_token
    ass = Merchant.objects.filter(alin_account=username, private_token=private_token)
    if ass.exists():
        return True
    else:
        return False


def datetime_to_string(datetimet):
    return str(timezone.localtime(datetimet))