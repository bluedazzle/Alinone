import datetime
import string
import time
import random
import requests
import json
from CronOrder.models import *
from AlinLog.models import *
from django.http import Http404

def createAlinOrderNum(platid,merchantid,autoid):
    odate = datetime.date.today()
    odate = str(odate).replace('-', '')
    auto_format = ''
    plat_format = ''
    merchant_format = ''
    if len(str(platid)) <= 2 and len(str(merchantid)) <= 8:
        auto_format = '%04i' % int(autoid)
        plat_format = '%02i' % int(platid)
        merchant_format = '%08i' % int(merchantid)
    else:
        return 0
    aon = str(odate) + plat_format + merchant_format + auto_format
    return aon

def resetAutoId(args = None):
    merlist = Merchant.objects.all()
    for itm in merlist:
        itm.todaynum = 1
        itm.save()
    content = 'success reset todaynum'
    print content
    newlog = CronLog()
    newlog.ltype = 4
    newlog.content = content
    newlog.status = True
    newlog.save()
    return True

def createMeiId():
    return string.join(random.sample('FEDCBA1234567890FEDCBA1234567890FEDCBA1234567890FEDCBA1234567890', 64)).replace(" ", "")

def createMeiOrder(mid):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))[2:]
    mmid = '%07i' % int(mid)
    mei_id = date + mmid + '0000'
    return mei_id

def timestampToDatetime(timestamp):
    formattime = time.localtime(float(timestamp))
    datetimee = datetime.datetime(*formattime[:6])
    return datetimee



def get_phone_belong(phone):
    url = 'http://api.k780.com:88/?app=phone.get&appkey=13790&sign=40003a34260aa4def35d83d83a7ba580&format=json&phone=' + str(phone)
    newreq = requests.get(url, timeout=6)
    res = newreq.content
    # try:
    jsonres = json.loads(res)
    if str(jsonres['success']) == '1':
        return jsonres['result']['style_simcall']
    return 'fail'
    # except:
    #     return 'fail'


