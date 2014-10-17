from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.template import Template,Context
from django.views.decorators.csrf import csrf_exempt
import simplejson
import datetime
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
            current_user = Sender.objects.get(phone = str(privatetoken))
            if current_user is not None:
                bind_merchant = Merchant.objects.get(id = int(merchantid))
                if bind_merchant is not None:
                    body['merchant_name'] = bind_merchant.name
                    body['merchant_id'] = bind_merchant.id
                    return HttpResponse(encodejson(1, body))
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
def unbindmerchant(req):
    body = {}
    if req.method == 'POST':
        reqdata = simplejson.loads(req.body)
        merchantid = reqdata['merchant_id']
        privatetoken = reqdata['private_token']
        currentuser = Sender.objects.get(phone = str(privatetoken))
        if currentuser is not None:
            unbindm = Merchant.objects.get(id = int(merchantid))
            unbindm.bind_sender.remove(currentuser)
            unbindm.save()
            return HttpResponse(encodejson(1, body))
        else:
            return HttpResponse(encodejson(7, body))
    else:
        raise Http404

def finishorder(req):
    body = {}
    if req.method == 'POST':
        orderobjlist = []
        reqdata = simplejson.loads(req.body)
        privatetoken = reqdata['private_token']
        #orderlist = reqdata['orders_id']
        currentuser = Sender.objects.get(phone = str(privatetoken))
        if currentuser is not None:
            curentorders = currentuser.DayOrder_set.all()
            for item in curentorders:
                item.status =
            currentuser.DayOrder_set.clear()
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

def


def encodejson(status, body):
    tmpjson = {}
    tmpjson['status'] = status
    tmpjson['body'] = body
    return simplejson.dumps(tmpjson)

def testindex(req):
    t = 'It works!'
    return HttpResponse(t)