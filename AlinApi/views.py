from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.template import Template,Context
from django.views.decorators.csrf import csrf_exempt
import simplejson
import datetime
import random
import string
import copy
from AlinApi.object import *
from CronOrder.models import *
# Create your views here.

@csrf_exempt
def bindmerchant(req):
    body = {}
    #try:
    if req.method == 'POST':
        reqdata = simplejson.loads(req.body)
        timestamp = reqdata['time_stamp']
        merchantid = reqdata['merchant_id']
        privatetoken = reqdata['private_token']
        reqtime = datetime.datetime.fromtimestamp(timestamp)
        now = datetime.datetime.now()
        detla = now - reqtime
        if detla <= datetime.timedelta(seconds = 300):
            current_user = Sender.objects.get(private_token = str(privatetoken))
            if current_user is not None:
                lasttime = current_user.active_time.replace(tzinfo = None)
                if not isactive(lasttime):
                    return HttpResponse(encodejson(5, body))
                current_user.active_time = datetime.datetime.utcnow()
                current_user.save()
                bind_merchant = Merchant.objects.get(id = int(merchantid))
                if bind_merchant is not None:
                    if current_user not in bind_merchant.bind_sender.all():
                        bind_merchant.bind_sender.add(current_user)
                        body['merchant_name'] = bind_merchant.name
                        body['merchant_id'] = bind_merchant.id
                        bind_merchant.save()
                        return HttpResponse(encodejson(1, body))
                    else:
                        return HttpResponse(encodejson(6, body))
                else:
                    return HttpResponse(encodejson(7, body))
            else:
                return HttpResponse(encodejson(7, body))
        else:
            return HttpResponse(encodejson(5, body))
    else:
        return HttpResponse('no get')
    #except:
     #   return HttpResponse('error')
    #finally:
     #   pass

@csrf_exempt
def unbindmerchant(req):
    body = {}
    if req.method == 'POST':
        reqdata = simplejson.loads(req.body)
        merchantid = reqdata['merchant_id']
        privatetoken = reqdata['private_token']
        currentuser = Sender.objects.get(private_token = str(privatetoken))
        if currentuser is not None:
            lasttime = currentuser.active_time.replace(tzinfo = None)
            if not isactive(lasttime):
                return HttpResponse(encodejson(5, body))
            currentuser.active_time = datetime.datetime.utcnow()
            currentuser.save()
            unbindm = Merchant.objects.get(id = int(merchantid))
            unbindm.bind_sender.remove(currentuser)
            unbindm.save()
            return HttpResponse(encodejson(1, body))
        else:
            return HttpResponse(encodejson(7, body))

    else:
        raise Http404

@csrf_exempt
def finishorder(req):
    body = {}
    if req.method == 'POST':
        orderidlist = []
        reqdata = simplejson.loads(req.body)
        privatetoken = reqdata['private_token']
        orderlist = reqdata['orders_id']
        currentuser = Sender.objects.get(private_token = str(privatetoken))
        if currentuser is not None:
            lasttime = currentuser.active_time.replace(tzinfo = None)
            if not isactive(lasttime):
                return HttpResponse(encodejson(5, body))
            currentuser.active_time = datetime.datetime.utcnow()
            currentuser.save()
            curentorders = currentuser.order.all()
            if orderlist is not None:
                for itm in orderlist:
                    orderidlist.append(copy.copy(itm['order_id']))
                for item in curentorders:
                    if str(item.order_id_alin) not in orderidlist:
                        item.finish_by = str(currentuser.phone)
                        item.status = 4
                        item.save()
            else:
                for item in currentorders:
                    item.finish_by = str(currentuser.phone)
                    item.status = 4
                    item.save()
            currentuser.order.clear()
            currentuser.save()
            return HttpResponse(encodejson(1, body))
            #if
            #for itm in orderlist:
            #    newobj = DayOrder.objects.get(order_id_alin = str(itm['order_id']))
            #    if newobj is not None:
        else:
            return HttpResponse(encodejson(7, body))
    else:
        raise Http404

@csrf_exempt
def renewgps(req):
    body = {}
    if req.method == 'POST':
        reqdata = simplejson.loads(req.body)
        lng = reqdata['lng']
        lat = reqdata['lat']
        privatetoken = reqdata['private_token']
        nowtime = datetime.datetime.utcnow()
        currentuser = Sender.objects.get(private_token = str(privatetoken))
        if currentuser is not None:
            lasttime = currentuser.active_time.replace(tzinfo = None)
            if not isactive(lasttime):
                return HttpResponse(encodejson(5, body))
            currentuser.lng = float(lng)
            currentuser.lat = float(lat)
            currentuser.active_time = nowtime
            currentuser.update_time = nowtime
            currentuser.save()
            return HttpResponse(encodejson(1, body))
        else:
            return HttpResponse(encodejson(7, body))
    else:
        raise Http404

@csrf_exempt
def bindorders(req):
    body = {}
    status = 1
    faillist = []
    if req.method == 'POST':
        reqdata = simplejson.loads(req.body)
        orderlist = reqdata['orders_id']
        privatetoken = reqdata['private_token']
        currentuser = Sender.objects.get(private_token = str(privatetoken))
        if currentuser is not None:
            lasttime = currentuser.active_time.replace(tzinfo = None)
            if not isactive(lasttime):
                return HttpResponse(encodejson(5, body))
            currentuser.active_time = datetime.datetime.utcnow()
            currentuser.save()
            for itm in orderlist:
                bindorder = DayOrder.objects.get(order_id_alin = str(itm['order_id']))
                if bindorder is not None:
                    print currentuser.sender.all()
                    print bindorder.merchant
                    if bindorder.merchant in currentuser.sender.all():
                        bindorder.bind_sender = currentuser
                        bindorder.save()
                    else:
                        status = 13
                        faillist.append(copy.copy(itm['order_id']))
                        continue
                else:
                    status = 4
                    faillist.append(copy.copy(itm['order_id']))
            body['fail_list'] = faillist
            return HttpResponse(encodejson(status, body))
        else:
            return HttpResponse(encodejson(7, body))
    else:
        raise Http404

@csrf_exempt
def senderinfo(req):
    body = {}
    merchantlist = []
    if req.method == 'POST':
        reqdata = simplejson.loads(req.body)
        privatetoken = reqdata['private_token']
        currentuser = Sender.objects.get(private_token = str(privatetoken))
        if currentuser is not None:
            lasttime = currentuser.active_time.replace(tzinfo = None)
            if not isactive(lasttime):
                return HttpResponse(encodejson(5, body))
            currentuser.active_time = datetime.datetime.utcnow()
            currentuser.save()
            bindmerchants = currentuser.sender.all()
            for itm in bindmerchants:
                finishorders = DayOrder.objects.filter(finish_by = str(currentuser.phone), merchant = itm)
                newinfo = {}
                newinfo['merchant_id'] = '%08i' % itm.id
                newinfo['merchant_name'] = itm.name
                newinfo['sended'] = int(finishorders.count())
                merchantlist.append(copy.copy(newinfo))
            body['merchants'] = merchantlist
            return HttpResponse(encodejson(1, body))
        else:
            return HttpResponse(encodejson(7, body))
    else:
        raise Http404

@csrf_exempt
def login(req):
    body = {}
    if req.method == 'POST':
        reqdata = simplejson.loads(req.body)
        username = reqdata['username']
        passwd = reqdata['password']
        sender = Sender.objects.get(phone = str(username))
        if sender is not None:
            if sender.passwd == passwd:
                mytoken = createtoken()
                sender.private_token = mytoken
                sender.active_time = datetime.datetime.utcnow()
                sender.save()
                body["private_token"] = mytoken
                return HttpResponse(encodejson(1, body))
            else:
                return HttpResponse(encodejson(4, body))
        else:
            return HttpResponse(encodejson(7, body))
    else:
        raise Http404

@csrf_exempt
def register(req):
    body = {}
    if req.method == 'POST':
        reqdata = simplejson.loads(req.body)
        username = reqdata['username']
        passwd = reqdata['password']
        code = reqdata['reg_code']
        ishave = Sender.objects.filter(phone = str(username))
        if ishave.count() == 0:
            if code == '1234':
                mytoken = createtoken()
                newsender = Sender()
                newsender.phone = username
                newsender.passwd = passwd
                newsender.active_time = datetime.datetime.utcnow()
                newsender.private_token = mytoken
                newsender.save()
                body["private_token"] = mytoken
                return HttpResponse(encodejson(1, body))
            else:
                return HttpResponse(encodejson(12, body))
        else:
            return HttpResponse(encodejson(6, body))
    else:
        raise Http404

def isactive(lastactivetime, det=600):
    print lastactivetime
    nowt = datetime.datetime.utcnow()
    detla = nowt - lastactivetime
    if detla > datetime.timedelta(seconds=det):
        return False
    else:
        return True


def encodejson(status, body):
    tmpjson = {}
    tmpjson['status'] = status
    tmpjson['body'] = body
    return simplejson.dumps(tmpjson)

def createtoken(count = 32):
    return string.join(random.sample('ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba~+=', count)).replace(" ", "")

def testindex(req):
    t = 'It works!'
    return HttpResponse(t)