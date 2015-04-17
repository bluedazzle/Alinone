# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
from AlinLog.models import AccountLog
from merchant_page.models import *
from CronOrder.Aaps import *
from CronOrder.ALO import *
import json
import time
import simplejson
import hashlib
import datetime
alo = Alo()
# aps = OrderAps()

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
                if user.verify is False:
                    return render_to_response('login_page.html', {'flag': 2}, context_instance=RequestContext(request))
                request.session['username'] = user_name
                merchant = Merchant.objects.get(alin_account=user_name)
                merchant.update_time = datetime.datetime.now()
                merchant.is_online = True
                merchant.save()
                newlog = AccountLog()
                newlog.atype = '商家'
                newlog.content = '商家登陆'
                newlog.ltype = 11
                newlog.note = '登陆'
                newlog.account = str(user_name)
                newlog.save()
                return HttpResponseRedirect("/merchant/operate_new")
            else:
                return render_to_response('login_page.html', {'flag': 1}, context_instance=RequestContext(request))
        except Merchant.DoesNotExist:
            return render_to_response('login_page.html', {'flag': 1}, context_instance=RequestContext(request))
    else:
        return render_to_response('login_page.html', context_instance=RequestContext(request))

# def apstest(req):
#     global aps
#     aps.stopAps()
#     return HttpResponse('success stop aps task')

#登出函数
def login_out(request):
    user_name = request.session.get('username')
    merchant = Merchant.objects.get(alin_account=user_name)
    merchant.is_online = False
    merchant.save()
    newlog = AccountLog()
    newlog.atype = '商家'
    newlog.content = '商家登出'
    newlog.ltype = 12
    newlog.note = '登出'
    newlog.account = str(user_name)
    newlog.save()
    del request.session['username']
    return HttpResponseRedirect("login_in")

#忘记密码操作
def forget_password(request):
    if request.method == 'GET':
        return render_to_response('forget_password.html', context_instance=RequestContext(request))
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
                                                                'fault1': 'T'}, context_instance=RequestContext(request))
                else:
                    merchant = Merchant.objects.get(alin_account=phone)
                    merchant.password = hashlib.md5(password).hexdigest()
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
        context = {}
        context.update(csrf(request))
        phone = request.POST.get('phone')
        merchant_have = Merchant.objects.filter(alin_account=phone)
        if merchant_have.count() > 0:
            # print 'aa'
            req = createverfiycode(phone)
            print req
            newlog = AccountLog()
            newlog.atype = '商家'
            newlog.content = '商家忘记密码'
            newlog.ltype = 13
            newlog.note = '忘密'
            newlog.account = str(phone)
            newlog.save()
            return HttpResponse(json.dumps("OK"), content_type="application/json")
        else:
            return HttpResponse(json.dumps("False"), content_type="application/json")
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
            phone_verify = PhoneVerify.objects.filter(phone=str(phone), verify_code=str(verify))
            if phone_verify.count() > 0:
                update_time = phone_verify[0].update_time
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
                    newlog = AccountLog()
                    newlog.atype = '商家'
                    newlog.content = '商家注册'
                    newlog.ltype = 14
                    newlog.note = '注册'
                    newlog.account = str(phone)
                    newlog.save()
                    return render_to_response('login_page.html', {'flag': 2}, context_instance=RequestContext(request))
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
            return HttpResponse(json.dumps("false"), content_type="application/json")
        req = createverfiycode(phone)
        print req
        return HttpResponse(json.dumps("true"), content_type="application/json")
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
            newlog = AccountLog()
            newlog.atype = '商家'
            newlog.content = '商家更改密码'
            newlog.ltype = 16
            newlog.note = '改密'
            newlog.account = str(phone)
            newlog.save()
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
            newlog = AccountLog()
            newlog.atype = '商家'
            newlog.content = '商家更改名称'
            newlog.ltype = 15
            newlog.note = '改名'
            newlog.account = str(phone)
            newlog.save()
            return render_to_response('change_name.html', {'success': 'T', 'new_user_name': new_name}, context_instance=RequestContext(request))
        else:
            return render_to_response('change_name.html', {'phone': phone, 'new_name': new_name}, context_instance=RequestContext(request))


#get orders count
def get_orders_count(request):
    # global alo
    # res = None
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')
    else:
        merchant_id = request.session['username']
        merchant = Merchant.objects.get(alin_account=merchant_id)
        merchant.update_time = datetime.datetime.now()
        merchant.save()
        # if merchant.tao_account != '' or merchant.ele_account != '' or merchant.mei_account != '':
        #     res = alo.cronOrder(str(merchant.id))
        #     print res
        status = 'T'
        if merchant.tao_account:
            if merchant.tao_status == False:
                status = 'F'
        if merchant.ele_account:
            if merchant.ele_status == False:
                status = 'F'
        if merchant.mei_account:
            if merchant.mei_status == False:
                status = 'F'
        order_list = DayOrder.objects.filter(merchant=merchant, status=1)
        finish_list = DayOrder.objects.filter(merchant=merchant, status=4)
        finnum = finish_list.count()
        total = 0.0
        res = True
        for it in finish_list:
            total += float(it.real_price)
        if order_list.count() == 0:
            count = 'N'
        else:
            count = order_list.count()
        notice_list = Notice.objects.all()
        total = '%.2f' % total
        if notice_list.count() > 0:
            notice_list0 = []
            for item in notice_list:
                notice_list0.append(item.content)
            content = {'count': count,
                       'status': status,
                       'order_num': finnum,
                       'total_money': total,
                       'ver': res,
                       'notice_list': notice_list0}
        else:
            content = {'count': count,
                       'status': status,
                       'order_num': finnum,
                       'total_money': total,
                       'ver': res,
                       'notice_list': 'N'}
        return HttpResponse(simplejson.dumps(content), content_type="application/json")



def asyalo(request, first=False):
    global alo
    res = None
    if request.session.get('username'):
        merchant_id = request.session['username']
        merchant = Merchant.objects.get(alin_account=merchant_id)
        if merchant.tao_account != '' or merchant.ele_account != '' or merchant.mei_account != '':
            res = alo.cronOrder(str(merchant.id), first)
            print res
    return HttpResponse('True')



# def asy_get_counts(request):
#     if not request.session.get('username'):
#         return HttpResponseRedirect('login_in')
#     else:
#         merchant_id = request.session['username']
#         # merchant = Merchant.objects.get(alin_account=merchant_id)
#         gevent.joinall([gevent.spawn(asyalo, merchant_id),
#                         gevent.spawn(get_orders_count, request)])


#进入未处理订单界面
def operate_new(request):
    if request.method == 'GET':
        if request.session.get('username'):
            order_detail = []
            dish_list = []
            try:
                merchant0 = request.session.get('username')
                merchant = Merchant.objects.get(alin_account=merchant0)
                merchant.update_time = datetime.datetime.now()
                merchant.save()
                order_detail = DayOrder.objects.order_by('-id').filter(merchant=merchant, status=1)
                request.session['new_order_id'] = order_detail[0].id
                dish_list = Dish.objects.all
                order_detail = pingtai_name(order_detail)
                paginator = Paginator(order_detail, 20)
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
                                                                    'user_name': merchant.name, 'merchant': merchant},
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
        merchant.update_time = datetime.datetime.now()
        merchant.save()
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
                merchant.update_time = datetime.datetime.now()
                merchant.save()
                order_detail = DayOrder.objects.order_by('-order_time').filter(merchant=merchant, status=2)
                order_detail = pingtai_name(order_detail)
                paginator = Paginator(order_detail, 20)
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
    if request.method == 'GET':
        merchant_id = request.session['username']
        merchant = Merchant.objects.get(alin_account=merchant_id)
        merchant.update_time = datetime.datetime.now()
        merchant.save()
        express_people = merchant.bind_sender.all()
        orders = DayOrder.objects.order_by('-order_time').filter(merchant=merchant, status=3)
        orders = pingtai_name(orders)
        sender_orders = []
        sender_id = request.GET.get('id')
        sender = ''
        if sender_id:
            for person in express_people:
                if person.id == int(sender_id):
                    sender = person
        else:
            try:
                sender = express_people[0]
            except:
                sender = []
        for item in orders:
            if item.bind_sender == sender:
                sender_orders.append(item)

        paginator = Paginator(sender_orders, 20)
        try:
            page_num = request.GET.get('page')
            sender_orders = paginator.page(page_num)
        except PageNotAnInteger:
            sender_orders = paginator.page(1)
        except EmptyPage:
            sender_orders = paginator.page(paginator.num_pages)
        except:
            pass
        return render_to_response('merchant_operate_paisong.html', {'orders': sender_orders,
                                                                    'express_people': express_people,
                                                                    'sender': sender}
                                  , context_instance=RequestContext(request))


def operate_finish(request):
    if request.method == 'GET':
        if request.session.get('username'):
            try:
                merchant0 = request.session.get('username')
                merchant = Merchant.objects.get(alin_account=merchant0)
                merchant.update_time = datetime.datetime.now()
                merchant.save()
                order_detail = DayOrder.objects.order_by('-order_time').filter(merchant=merchant, status=4)
                order_detail = pingtai_name(order_detail)
                paginator = Paginator(order_detail, 20)
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
            return render_to_response('merchant_operate_finish.html', {'items': order_detail}, context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect("login_in")
    return render_to_response('merchant_operate_finish.html', context_instance=RequestContext(request))

#进入平台管理页面
def operate_pingtai(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')
    merchant_id = request.session['username']
    merchant = Merchant.objects.get(alin_account=merchant_id)
    merchant.update_time = datetime.datetime.now()
    if request.method == 'GET':
        if request.GET.has_key('top_session'):
            tdd_session = request.REQUEST.get('top_session')
            merchant.tao_sessionkey = str(tdd_session)
            merchant.tao_account = '已绑定'
    merchant.save()
    items = []
    if merchant.tao_account:
        item = {'name': '1',
                'account': merchant.tao_account,
                'status': merchant.tao_status,
                'message': merchant.tao_message}
        items.append(item)
    if merchant.mei_account:
        item = {'name': '3',
                'account': merchant.mei_account,
                'status': merchant.mei_status,
                'message': merchant.mei_message}
        items.append(item)
    if merchant.ele_account:
        item = {'name': '2',
                'account': merchant.ele_account,
                'status': merchant.ele_status,
                'message': merchant.ele_message}
        items.append(item)

    return render_to_response('merchant_operate_pingtai.html', {'items': items}, context_instance=RequestContext(request))


#进入删除订单页面
def operate_delete(request):
    if request.method == 'GET':
        if request.session.get('username'):
            try:
                merchant0 = request.session.get('username')
                merchant = Merchant.objects.get(alin_account=merchant0)
                merchant.update_time = datetime.datetime.now()
                merchant.save()
                order_detail = DayOrder.objects.order_by('-order_time').filter(merchant=merchant, status=5)
                order_detail = pingtai_name(order_detail)
                paginator = Paginator(order_detail, 20)
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
    merchant.update_time = datetime.datetime.now()
    merchant.save()
    express_people = merchant.bind_sender.all()
    return render_to_response('merchant_operate_express_person.html', {'express_people': express_people}, context_instance=RequestContext(request))


#打印机设置页面
def printer_setting(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')
    merchant_id = request.session['username']
    merchant = Merchant.objects.get(alin_account=merchant_id)
    auto_print_status = request.GET.get('auto_print_status')
    if auto_print_status:
        if auto_print_status == 'T':
            merchant.auto_print = True
            merchant.save()
            print 'yes'
        elif auto_print_status == 'F':
            merchant.auto_print = False
            merchant.save()
        else:
            print 'no'
    else:
        print 'NNN'
    if merchant.auto_print:
        flag = 'T'
    else:
        flag = 'F'
    return render_to_response('merchant_printer_setting.html', {'flag': flag}, context_instance=RequestContext(request))


#加载平台名称
def pingtai_name(orders):
    for item in orders:
        if item.platform == 1:
            item.platform = "淘点点"
        elif item.platform == 3:
            item.platform = "美团"
        elif item.platform == 2:
            item.platform = "饿了么"
        elif item.platform == 10:
            item.platform = "电话订单"
        elif item.platform == 11:
            item.platform = "其他平台"
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
        merchant.update_time = datetime.datetime.now()
        merchant.save()
        order_detail = DayOrder.objects.filter(merchant=merchant, status=1)
        return render_to_response('print_all.html', {'items': order_detail}, context_instance=RequestContext(request))
    except DayOrder.DoesNotExist:
        pass


#删除平台
def platform_delete(request, name):
    merchant_id = request.session['username']
    merchant = Merchant.objects.get(alin_account=merchant_id)
    merchant.update_time = datetime.datetime.now()
    cat_mer_list = CatcheData.objects.filter(merchant=merchant)
    cat_mer = None
    if cat_mer_list.count()>0:
        cat_mer = cat_mer_list[0]
    if name == '1':
        merchant.tao_account = ''
        merchant.tao_passwd = ''
        merchant.tao_sessionkey = ''
        merchant.tao_refreshkey = ''
        merchant.tao_message = ''
        merchant.tao_status = True
        merchant.save()
    elif name == '3':
        merchant.mei_account = ''
        merchant.mei_passwd = ''
        merchant.mei_message = ''
        merchant.mei_status = True
        merchant.save()
        if cat_mer is not None:
            cat_mer.mei_token = ""
            cat_mer.save()
    elif name == '2':
        merchant.ele_account = ''
        merchant.ele_passwd = ''
        merchant.ele_message = ''
        merchant.ele_status = True
        merchant.save()
        if cat_mer is not None:
            cat_mer.ele_cookie = ''
            cat_mer.save()
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
    merchant.update_time = datetime.datetime.now()
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
    asyalo(request, True)
    return HttpResponseRedirect('operate_pingtai')


#删除物流人员
def delete_sender(request, phone):
    merchant_id = request.session['username']
    merchant = Merchant.objects.get(alin_account=merchant_id)
    merchant.update_time = datetime.datetime.now()
    sender = Sender.objects.get(phone=phone)
    merchant.bind_sender.remove(sender)
    merchant.save()
    return HttpResponseRedirect("operate_express_person")


#进入添加物流人员页面
def add_sender_page(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')
    else:
        merchant_id = request.session['username']
        merchant = Merchant.objects.get(alin_account=merchant_id)
        merchant.update_time = datetime.datetime.now()
        merchant.save()
        express_people = merchant.bind_sender.all()
        request.session['sender_count'] = express_people.count()
        if request.GET.get('flag'):
            filename = request.session['qr_bind']
        else:
            qr_bind = createqr(2, merchant.id)
            request.session['qr_bind'] = qr_bind
            filename = qr_bind
        return render_to_response('merchant_add_sender.html', {'express_people': express_people, 'filename': filename})


#get sender change
def get_sender_change(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')
    else:
        merchant_id = request.session['username']
        merchant = Merchant.objects.get(alin_account=merchant_id)
        express_people = merchant.bind_sender.all()
        if request.session.get('sender_count') or request.session['sender_count'] == 0:
            if request.session['sender_count'] == express_people.count():
                return HttpResponse(json.dumps('F'), content_type="application/json")
            else:
                return HttpResponse(json.dumps('T'), content_type="application/json")

        else:
            return HttpResponse(json.dumps('T'), content_type="application/json")

def operate_today(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')
    merchant_id = request.session['username']
    currentuser = Merchant.objects.get(alin_account=merchant_id)
    pending = DayOrder.objects.filter(merchant=currentuser, status=1).count()
    accept = DayOrder.objects.filter(merchant=currentuser, status=2).count()
    sending = DayOrder.objects.filter(merchant=currentuser, status=3).count()
    refuse = DayOrder.objects.filter(merchant=currentuser, status=5).count()
    online = DayOrder.objects.filter(merchant=currentuser, status=4, pay=True).count()
    offline = DayOrder.objects.filter(merchant=currentuser, status=4, pay=False).count()
    tdd = DayOrder.objects.filter(merchant=currentuser, status=4, platform=1).count()
    ele = DayOrder.objects.filter(merchant=currentuser, status=4, platform=2).count()
    mei = DayOrder.objects.filter(merchant=currentuser, status=4, platform=3).count()
    other = DayOrder.objects.filter(merchant=currentuser, status=4, platform=4).count()
    total_orders = DayOrder.objects.filter(merchant=currentuser, status=4)
    online_money = 0.0
    offline_money = 0.0
    for itm in total_orders:
        if itm.pay is False:
            offline_money += float(itm.real_price)
        else:
            online_money += float(itm.real_price)
    total_money = online_money + offline_money
    summary = '今日待接收' + str(pending) + '单，已接收' + str(accept) + '单，派送中' + str(sending) + '单，已撤销' + str(refuse) + '单，已完成' + str(total_orders.count()) + '单，其中，淘点点' + str(tdd) + '单，饿了么' + str(ele) + '单，美团' + str(mei) + '单，其他' + str(other) + '单，线上支付' + str(online) + '单，共计' + str(online_money) + '元，线下支付' + str(offline) + '单，共计' + str(offline_money) + '元，今日总营业额' + str(total_money) + '元'
    senders = currentuser.bind_sender.all()
    for item in senders:
        my_send = DayOrder.objects.filter(finished_by=item)
        my_sending = DayOrder.objects.filter(bind_sender=item).count()
        if my_sending == 0:
            item.status = '待命中'
        else:
            item.status = '派送中'
        item.today_sends = int(my_send.count())
        for itm in my_send:
            if itm.pay is False:
                item.offline_money += float(itm.real_price)
                item.offline_num += 1
            else:
                item.online_money += float(itm.real_price)
                item.online_num += 1
    paginator = Paginator(senders, 20)
    try:
        page_num = request.GET.get('page')
        senders = paginator.page(page_num)
    except PageNotAnInteger:
        senders = paginator.page(1)
    except EmptyPage:
        senders = paginator.page(paginator.num_pages)
    except:
        pass
    return render_to_response('merchant_operate_today.html', {'senders': senders, 'summary': summary})

def operate_history(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')
    if request.method == 'GET':
        merchant_id = request.session['username']
        currentuser = Merchant.objects.get(alin_account=merchant_id)
        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')
        pagepara = '?end_date=' + start_date + '&start_date=' + end_date
        if start_date != '' and end_date != '':
            stime = time.strptime(start_date, "%Y-%m-%d")
            etime = time.strptime(end_date, "%Y-%m-%d")
            sdate = datetime.datetime(*stime[:6])
            edate = datetime.datetime(*etime[:6])
            total_orders = TotalOrder.objects.order_by('-order_time').filter(merchant=currentuser, order_time__range=(sdate, edate))
            senders = currentuser.bind_sender.all()
            paginator = Paginator(total_orders, 20)
            try:
                page_num = request.GET.get('page')
                total_orders = paginator.page(page_num)
            except PageNotAnInteger:
                total_orders = paginator.page(1)
            except EmptyPage:
                total_orders = paginator.page(paginator.num_pages)
            except:
                pass
            return render_to_response('merchant_operate_history.html', {'orders': total_orders, 'pagepara': pagepara})
        else:
            return render_to_response('merchant_operate_history.html')
    else:
        raise Http404