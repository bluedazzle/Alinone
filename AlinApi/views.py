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
def bindMerchant(req):
    body = {}
    return_json = {}
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
                bind_merchant = Merchant.objects.get(id = merchantid)
                if bind_merchant is not None:
                    body['merchant_name'] = bind_merchant.name
                    body['merchant_id'] = bind_merchant.id
                    return_json['status'] = 1
                    return_json['body'] = body
                    return HttpResponse(simplejson.dumps(return_json))
                else:
                    return_json['status'] = 7
                    return_json['body'] = body
                    return HttpResponse(simplejson.dumps(return_json))
            else:
                return_json['status'] = 7
                return_json['body'] = body
                return HttpResponse(simplejson.dumps(return_json))
        else:
            return_json['status'] = 5
            return_json['body'] = body
            return HttpResponse(simplejson.dumps(return_json))
    else:
        return HttpResponse('no get')
    #except:
     #   return HttpResponse('error')
    #finally:
     #   pass

def testindex(req):
    t = 'It works!'
    return HttpResponse(t)