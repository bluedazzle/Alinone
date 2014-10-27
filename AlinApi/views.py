from django.http import HttpResponse
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from AlinApi.fixlnglat import *
from AlinApi.method import *
import simplejson
import datetime
import random
import string
import copy
from CronOrder.models import *
# Create your views here.

gpsc = GpsCorrect()

@csrf_exempt
def bindmerchant(req):
    body = {}
    #try:
    if req.method == 'POST':
        print str(req.body)
        reqdata = simplejson.loads(req.body)
        timestamp = reqdata['time_stamp']
        merchantid = reqdata['merchant_id']
        privatetoken = reqdata['private_token']
        reqtime = datetime.datetime.fromtimestamp(float(timestamp))
        now = datetime.datetime.now()
        detla = now - reqtime
        if detla <= datetime.timedelta(seconds = 300):
            current_user = Sender.objects.get(private_token = str(privatetoken))
            if current_user is not None:
                lasttime = current_user.active_time.replace(tzinfo = None)
                if not isactive(lasttime):
                    return HttpResponse(encodejson(5, body), content_type="application/json")
                current_user.active_time = datetime.datetime.now()
                current_user.save()
                bind_merchant = Merchant.objects.get(id = int(merchantid))
                if bind_merchant is not None:
                    if current_user not in bind_merchant.bind_sender.all():
                        bind_merchant.bind_sender.add(current_user)
                        body['merchant_name'] = bind_merchant.name
                        body['merchant_id'] = str('%08i' % bind_merchant.id)
                        bind_merchant.save()
                        print body
                        return HttpResponse(encodejson(1, body), content_type="application/json")
                    else:
                        return HttpResponse(encodejson(6, body), content_type="application/json")
                else:
                    return HttpResponse(encodejson(7, body), content_type="application/json")
            else:
                return HttpResponse(encodejson(7, body), content_type="application/json")
        else:
            return HttpResponse(encodejson(5, body), content_type="application/json")
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
                return HttpResponse(encodejson(5, body), content_type="application/json")
            currentuser.active_time = datetime.datetime.now()
            currentuser.save()
            unbindm = Merchant.objects.get(id = int(merchantid))
            unbindm.bind_sender.remove(currentuser)
            unbindm.save()
            return HttpResponse(encodejson(1, body), content_type="application/json")
        else:
            return HttpResponse(encodejson(7, body), content_type="application/json")

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
                return HttpResponse(encodejson(5, body), content_type="application/json")
            currentuser.active_time = datetime.datetime.now()
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
            return HttpResponse(encodejson(1, body), content_type="application/json")
            #if
            #for itm in orderlist:
            #    newobj = DayOrder.objects.get(order_id_alin = str(itm['order_id']))
            #    if newobj is not None:
        else:
            return HttpResponse(encodejson(7, body), content_type="application/json")
    else:
        raise Http404

@csrf_exempt
def renewgps(req):
    body = {}
    if req.method == 'POST':
        reqdata = simplejson.loads(req.body)
        lng = float(reqdata['lng'])
        lat = float(reqdata['lat'])
        gcres = gpsc.transform(lat, lng)
        lng = gcres[1]
        lat = gcres[0]
        privatetoken = reqdata['private_token']
        nowtime = datetime.datetime.now()
        currentuser = Sender.objects.get(private_token = str(privatetoken))
        if currentuser is not None:
            lasttime = currentuser.active_time.replace(tzinfo = None)
            if not isactive(lasttime):
                return HttpResponse(encodejson(5, body), content_type="application/json")
            currentuser.lng = float(lng)
            currentuser.lat = float(lat)
            currentuser.active_time = nowtime
            currentuser.update_time = nowtime
            currentuser.save()
            return HttpResponse(encodejson(1, body), content_type="application/json")
        else:
            return HttpResponse(encodejson(7, body), content_type="application/json")
    else:
        raise Http404

@csrf_exempt
def bindorders(req):
    body = {}
    status = 1
    faillist = []
    bindlist = []
    if req.method == 'POST':
        reqdata = simplejson.loads(req.body)
        orderlist = reqdata['orders_id']
        privatetoken = reqdata['private_token']
        currentuser = Sender.objects.get(private_token = str(privatetoken))
        if currentuser is not None:
            lasttime = currentuser.active_time.replace(tzinfo = None)
            if not isactive(lasttime):
                return HttpResponse(encodejson(5, body), content_type="application/json")
            currentuser.active_time = datetime.datetime.now()
            currentuser.save()
            for itm in orderlist:
                bindorder = DayOrder.objects.get(order_id_alin = str(itm['order_id']))
                if bindorder is not None:
                    order = {}
                    # print currentuser.sender.all()
                    # print bindorder.merchant
                    if bindorder.merchant in currentuser.sender.all():
                        dishs = []
                        bindorder.bind_sender = currentuser
                        bindorder.status = 3
                        bindorder.save()
                        order['order_id'] = str(bindorder.order_id_alin)
                        order['name'] = str(bindorder.merchant.name)
                        order['merchant_id'] = str('%08i' % bindorder.merchant.id)
                        order['phone'] = str(bindorder.phone)
                        order['address'] = str(bindorder.address)
                        dishlist = bindorder.dishs.all()
                        for it in dishlist:
                            dish = {}
                            dish['name'] = it.dish_name
                            dish['count'] = it.dish_count
                            dish['price'] = it.dish_price
                            dishs.append(copy.copy(dish))
                        order['dish_list'] = dishs
                        bindlist.append(copy.copy(order))
                    else:
                        status = 13
                        faillist.append(copy.copy(itm['order_id']))
                        continue
                else:
                    status = 4
                    faillist.append(copy.copy(itm['order_id']))
            body['fail_list'] = faillist
            body['bind_list'] = bindlist
            return HttpResponse(encodejson(status, body), content_type="application/json")
        else:
            return HttpResponse(encodejson(7, body), content_type="application/json")
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
                return HttpResponse(encodejson(5, body), content_type="application/json")
            currentuser.active_time = datetime.datetime.now()
            currentuser.save()
            bindmerchants = currentuser.sender.all()
            for itm in bindmerchants:
                finishorders = DayOrder.objects.filter(finish_by = str(currentuser.phone), merchant = itm)
                newinfo = {}
                newinfo['merchant_id'] = str('%08i' % itm.id)
                newinfo['merchant_name'] = itm.name
                newinfo['sended'] = int(finishorders.count())
                merchantlist.append(copy.copy(newinfo))
            body['merchants'] = merchantlist
            return HttpResponse(encodejson(1, body), content_type="application/json")
        else:
            return HttpResponse(encodejson(7, body), content_type="application/json")
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
                sender.active_time = datetime.datetime.now()
                sender.save()
                body["private_token"] = mytoken
                return HttpResponse(encodejson(1, body), content_type="application/json")
            else:
                return HttpResponse(encodejson(4, body), content_type="application/json")
        else:
            return HttpResponse(encodejson(7, body), content_type="application/json")
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
                newsender.active_time = datetime.datetime.now()
                newsender.private_token = mytoken
                newsender.save()
                body["private_token"] = mytoken
                return HttpResponse(encodejson(1, body), content_type="application/json")
            else:
                return HttpResponse(encodejson(12, body), content_type="application/json")
        else:
            return HttpResponse(encodejson(6, body), content_type="application/json")
    else:
        raise Http404

@csrf_exempt
def searchmeal(req):
    iplist = ['127.0.0.1', 'localhost', '100.64.132.200', '125.71.229.18']
    body = {}
    meallist = []
    if req.method == 'GET':
        reqid = str(req.META['REMOTE_ADDR'])
        if reqid not in iplist:
            return HttpResponse(encodejson(9, body), content_type="application/json")
        searchstr = req.REQUEST.get('search')
        if searchstr is not None:
            if len(searchstr) == 22:
                meals = DayOrder.objects.filter(order_id_alin = str(searchstr))
            elif len(searchstr) == 11:
                meals = DayOrder.objects.filter(phone = str(searchstr))
            else:
                meals = DayOrder.objects.filter(phone = str(searchstr))
            if meals.count() == 0:
                return HttpResponse(encodejson(7, body), content_type="application/json")
            for itm in meals:
                mealdic = {}
                disharr = []
                mealdic['order_id'] = str(itm.order_id_alin)
                mealdic['phone'] = str(itm.phone)
                mealdic['name'] = itm.merchant.name
                mealdic['address'] = itm.merchant.address
                mealdic['status'] = itm.status
                mealdic['sender_name'] = str(itm.finish_by)
                mealdic['update_time'] = str(timezone.localtime(itm.order_time))
                dishlist = itm.dishs.all()
                for it in dishlist:
                    dish = {}
                    dish['name'] = it.dish_name
                    dish['count'] = it.dish_count
                    dish['price'] = it.dish_price
                    disharr.append(copy.copy(dish))
                mealdic['dishs'] = disharr
                if itm.status == 3:
                    if itm.bind_sender is None:
                        continue
                    mealdic['sender_name'] = itm.bind_sender.nick
                    if itm.bind_sender.update_time is None:
                        mealdic['isfirst'] = True
                        mealdic['update_time'] = str(timezone.localtime(itm.bind_sender.active_time))
                    else:
                        mealdic['update_time'] = str(timezone.localtime(itm.bind_sender.update_time))
                        mealdic['isfirst'] = False
                        mealdic['lng'] = itm.bind_sender.lng
                        mealdic['lat'] = itm.bind_sender.lat
                meallist.append(copy.copy(mealdic))
            body['meal_list'] = meallist
            print body
            return HttpResponse(encodejson(1, body), content_type="application/json")
        else:
            return HttpResponse(encodejson(7, body))
    else:
        raise Http404

@csrf_exempt
def changepasswd(req):
    if req.method == 'POST':
        body = {}
        reqdata = simplejson.loads(req.body)
        privatetoken = reqdata['private_token']
        passwd = reqdata['password']
        new_passwd = reqdata['new_password']
        currentuserset = Sender.objects.filter(private_token = privatetoken)
        if currentuserset.count() > 0:
            currentuser = currentuserset[0]
            lasttime = currentuser.active_time.replace(tzinfo = None)
            if not isactive(lasttime):
                return HttpResponse(encodejson(5, body), content_type="application/json")
            if str(currentuser.passwd) == str(passwd):
                currentuser.passwd = new_passwd
                currentuser.save()
                return HttpResponse(encodejson(1, body), content_type="application/json")
            else:
                return HttpResponse(encodejson(4, body), content_type="application/json")
        else:
            return HttpResponse(encodejson(7, body), content_type="application/json")
    else:
        raise Http404


def forgetpasswd(req):
    body = {}
    if req.method == 'POST':
        reqdata = simplejson.loads(req.body)
        phone = reqdata['phone']
        currentuserset = Sender.objects.filter(phone = phone)
        if currentuserset.count() > 0:
            currentuser = currentuserset[0]
            verify = createverfiycode()
            sendverifycode(verify, currentuser.phone)
            currentuser.is_verify = True
            currentuser.verify_code = verify
            currentuser.save()
            return HttpResponse(encodejson(1, body), content_type="application/json")
        else:
            return HttpResponse(encodejson(7, body), content_type="application/json")
    else:
        raise Http404

def newpassword(req):
    body={}
    if req.method == 'POST':
        reqdata = simplejson.loads(req.body)
        vercode = reqdata['verify_code']
        newpasswd = reqdata['new_password']
        phone = reqdata['phone']
        currentuserset = Sender.objects.filter(phone = phone)
        if currentuserset.count() > 0:
            currentuser = currentuserset[0]
            if str(currentuser.verfiy_code) == str(vercode):
                currentuser.passwd = newpasswd
                currentuser.is_verify = False
                currentuser.verify_code = ''
                currentuser.save()
                return HttpResponse(encodejson(1, body), content_type="application/json")
            else:
                return HttpResponse(encodejson(12, body), content_type="application/json")
        else:
            return HttpResponse(encodejson(7, body), content_type="application/json")
    else:
        raise Http404




def isactive(lastactivetime, det=600):
    print lastactivetime
    nowt = datetime.datetime.utcnow()
    print nowt
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
    return string.join(random.sample('ZYXWVUTSRQPONMLKJIHGFEDCBA1234567890zyxwvutsrqponmlkjihgfedcba+=', count)).replace(" ", "")

def testindex(req):
    t = 'It works!'
    return HttpResponse(t)
