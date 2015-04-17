# -*- coding: utf-8 -*-
from CronOrder.models import *
from AlinApi.models import PhoneVerify
from QRcode.method import *
from django.views.decorators.csrf import csrf_exempt
from AlinApi.decorater import api_times
from AlinApi.method import *
from CronOrder.endecy import *
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
from django.utils import timezone
from CronOrder.ALO import *
import simplejson
import sys
import copy
import math


@csrf_exempt
@api_times
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
@api_times
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
@api_times
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
        body['merchant_name'] = curuser.name
        return HttpResponse(encodejson(1, body), content_type='application/json')
    else:
        raise Http404


@csrf_exempt
@api_times
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
@api_times
def change_password(req):
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
    old_password = resjson['old_password']
    new_password = resjson['new_password']
    if curuser.check_password(old_password):
        curuser.password = hashlib.md5(new_password).hexdigest()
        curuser.save()
        body['msg'] = 'password changed success'
        return HttpResponse(encodejson(1, body), content_type='application/json')
    else:
        body['msg'] = 'password not correct'
        return HttpResponse(encodejson(4, body), content_type='application/json')



@csrf_exempt
@api_times
def new_password(req):
    body = {}
    if not req.method == 'POST':
        raise Http404
    resjson = simplejson.loads(req.body)
    verify_c = str(resjson['verify_code'])
    phone = resjson['phone']
    newpass = resjson['new_password']
    verify_list = PhoneVerify.objects.filter(phone=phone)
    if not verify_list.exists():
        body['msg'] = 'invalid verify code'
        return HttpResponse(encodejson(7, body), content_type='application/json')
    verify = verify_list[0]
    if str(verify.verify_code) == verify_c:
        verify.delete()
        me_list = Merchant.objects.filter(alin_account=phone)
        if not me_list.exists():
            body['msg'] = 'merchant does not exists'
            return HttpResponse(encodejson(7, body), content_type='application/json')
        curuser = me_list[0]
        curuser.password = hashlib.md5(newpass).hexdigest()
        new_token = createtoken()
        curuser.private_token = new_token
        curuser.save()
        body['msg'] = 'password resest success'
        body['private_token'] = new_token
        body['merchant_name'] = curuser.name
        body['username'] = phone
        return HttpResponse(encodejson(1, body), content_type='application/json')
    else:
        body['msg'] = 'verify code not correct'
        return HttpResponse(encodejson(12, body), content_type='application/json')




@csrf_exempt
@api_times
def change_info(req):
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
    merhcant_name = resjson['merchant_name']
    curuser.name = merhcant_name
    curuser.save()
    body['msg'] = 'merhcant info change success'
    return HttpResponse(encodejson(1, body), content_type='application/json')




@csrf_exempt
@api_times
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
    if curuser.ele_account != '':
        if curuser.ele_status:
            body['ele_status'] = True
        else:
            body['ele_status'] = False
            body['ele_message'] = curuser.ele_message
    else:
        body['ele_status'] = None
    if curuser.mei_account != '':
        if curuser.mei_status:
            body['mei_status'] = True
        else:
            body['mei_status'] = False
            body['mei_message'] = curuser.mei_message
    else:
        body['mei_status'] = None
    # if curuser.tao_account != '':
    #     if curuser.tao_status:
    #         body['tao_status'] = True
    #     else:
    #         body['tao_status'] = False
    # else:
    #     body['tao_status'] = None
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
    new_order_list = DayOrder.objects.filter(merchant=curuser)
    body['today_total'] = new_order_list.count()
    new_order_list = DayOrder.objects.filter(merchant=curuser, status=4)
    total_money = 0.0
    for itm in new_order_list:
        total_money += float(itm.real_price)
    body['total_money'] = total_money
    return HttpResponse(encodejson(1, body), content_type='application/json')



@csrf_exempt
@api_times
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
@api_times
def get_handle_orders(req):
    body = {}
    if not req.method == "POST":
        raise Http404
    resjson = simplejson.loads(req.body)
    username = resjson['username']
    token = resjson['private_token']
    if not if_legal(username, token):
        body['msg'] = 'auth failed'
        return HttpResponse(encodejson(13, body), content_type='application/json')
    curuser = Merchant.objects.get(alin_account=username)
    n_order_list = DayOrder.objects.filter(status=2, merchant=curuser)
    n_order_list |= DayOrder.objects.filter(status=3, merchant=curuser)
    n_order_list |= DayOrder.objects.filter(status=4, merchant=curuser)
    n_order_list |= DayOrder.objects.filter(status=5, merchant=curuser)
    total = n_order_list.count()
    total_page = math.ceil(float(total) / 20.0)
    paginator = Paginator(n_order_list, 20)
    page_num = 1
    try:
        page_num = int(resjson['page'])
        print 'wtf'
        n_order_list = paginator.page(page_num)
    except PageNotAnInteger:
        n_order_list = paginator.page(1)
    except EmptyPage:
        n_order_list = []
    except:
        n_order_list = paginator.page(page_num)
    order_list = model_serializer(n_order_list)
    for i, itm in enumerate(n_order_list):
        dishs = model_serializer(Dish.objects.filter(order=itm))
        bind_sender = model_serializer(itm.bind_sender, except_attr=('password', 'private_token'))
        order_list[i]['dishs'] = dishs
        order_list[i]['bind_sender'] = bind_sender
    body['order_list'] = order_list
    body['total_page'] = total_page
    body['total'] = total
    body['page'] = page_num
    return HttpResponse(encodejson(1, body), content_type='application/json')



@csrf_exempt
@api_times
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
@api_times
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
@api_times
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
    create_time = resjson['create_time']
    c_datetime = timestampToDatetime(create_time)
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
        order_time=c_datetime,
        send_time=c_datetime,
        qr_path=qr_path
    )
    new_order.save()
    body['msg'] = 'create new order success'
    return HttpResponse(encodejson(1, body), content_type='application/json')



@csrf_exempt
@api_times
def add_platform(req):
    body = {}
    if not req.method == 'POST':
        raise Http404
    resjson = simplejson.loads(req.body)
    username = resjson['username']
    token = resjson['private_token']
    if not if_legal(username, token):
        body['msg'] = 'login before other action'
        return HttpResponse(encodejson(13, body), content_type='application/json')
    curuser = Merchant.objects.get(alin_account=username)
    form_type = resjson['platform_type']
    form_account = resjson['account']
    form_password = resjson['password']
    password = Encrypt(form_password)
    if form_type == 2:
        if curuser.ele_account != '':
            body['msg'] = 'ele account exists'
            return HttpResponse(encodejson(6, body), content_type='application/json')
        curuser.ele_account = form_account
        curuser.ele_passwd = password
    elif form_type == 3:
        if curuser.mei_account != '':
            body['msg'] = 'met account exists'
            return HttpResponse(encodejson(6, body), content_type='application/json')
        curuser.mei_account = form_account
        curuser.mei_passwd = password
    curuser.save()
    alo = Alo()
    alo.cronOrder(str(curuser.id), True)
    body['msg'] = 'platform add success'
    return HttpResponse(encodejson(1, body), content_type='application/json')



@csrf_exempt
@api_times
def delete_platform(req):
    body = {}
    if not req.method == 'POST':
        raise Http404
    resjson = simplejson.loads(req.body)
    username = resjson['username']
    token = resjson['private_token']
    if not if_legal(username, token):
        body['msg'] = 'login before other action'
        return HttpResponse(encodejson(13, body), content_type='application/json')
    curuser = Merchant.objects.get(alin_account=username)
    cat_mer_list = CatcheData.objects.filter(merchant=curuser)
    cat_mer = None
    if cat_mer_list.count()>0:
        cat_mer = cat_mer_list[0]
    platform_id = resjson['platform_type']
    if platform_id == 2:
        curuser.ele_account = ''
        curuser.ele_passwd = ''
        curuser.ele_message = ''
        curuser.ele_status = True
        if cat_mer is not None:
            cat_mer.ele_cookie = ''
            cat_mer.save()
    elif platform_id == 3:
        curuser.mei_account = ''
        curuser.mei_status = True
        curuser.mei_message = ''
        curuser.mei_passwd = ''
        if cat_mer is not None:
            cat_mer.mei_token = ''
            cat_mer.save()
    curuser.save()
    body['msg'] = 'platform delete success'
    return HttpResponse(encodejson(1, body), content_type='application/json')



@csrf_exempt
@api_times
def add_sender(req):
    body = {}
    if not req.method == 'POST':
        raise Http404
    resjson = simplejson.loads(req.body)
    username = resjson['username']
    token = resjson['private_token']
    if not if_legal(username, token):
        body['msg'] = 'login before other action'
        return HttpResponse(encodejson(13, body), content_type='application/json')
    curuser = Merchant.objects.get(alin_account=username)
    res = createqr(2, curuser.id)
    body['bind_pic'] = res
    body['msg'] = 'get qrcode success'
    return HttpResponse(encodejson(1, body), content_type='application/json')


@csrf_exempt
@api_times
def delete_sender(req):
    body = {}
    if not req.method == 'POST':
        raise Http404
    resjson = simplejson.loads(req.body)
    username = resjson['username']
    sender_phone = resjson['sender']
    token = resjson['private_token']
    if not if_legal(username, token):
        body['msg'] = 'login before other action'
        return HttpResponse(encodejson(13, body), content_type='application/json')
    curuser = Merchant.objects.get(alin_account=username)
    sender_list = Sender.objects.filter(phone=sender_phone)
    if not sender_list.exists():
        body['msg'] = 'invalid sender phone'
        return HttpResponse(encodejson(7, body), content_type='application/json')
    sender = sender_list[0]
    bind_sender_list = curuser.bind_sender.all()
    if sender in bind_sender_list:
        curuser.bind_sender.remove(sender)
        body['msg'] = 'delete sender success'
        return HttpResponse(encodejson(1, body), content_type='application/json')
    else:
        body['msg'] = 'invalid sender'
        return HttpResponse(encodejson(7, body), content_type='application/json')



@csrf_exempt
@api_times
def get_senders(req):
    body = {}
    if not req.method == 'POST':
        raise Http404
    resjson = simplejson.loads(req.body)
    username = resjson['username']
    token = resjson['private_token']
    if not if_legal(username, token):
        body['msg'] = 'login before other action'
        return HttpResponse(encodejson(13, body), content_type='application/json')
    curuser = Merchant.objects.get(alin_account=username)
    bind_sender_list = curuser.bind_sender.all()
    sender_list = []
    for itm in bind_sender_list:
        sender = {}
        sender['phone'] = itm.phone
        sender['nick'] = itm.nick
        sender_list.append(copy.copy(sender))
    body['sender_list'] = sender_list
    body['msg'] = 'get sender list success'
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