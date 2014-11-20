import random
import simplejson
import string
import datetime
import urllib
from AlinApi.models import *
from AlinApi.yunpian import *
from CronOrder.NetSpider import *
import string

def createverfiycode(phone, count=6):
    result = {}
    vercode = string.join(random.sample('0123456789', count)).replace(" ", "")
    res = sendverifycode(vercode, phone)
    result['success'] = res
    result['verify_code'] = vercode
    jsonen = simplejson.dumps(result)
    return jsonen

def sendverifycode(content, phone):
    vf = NetSpider()
    vf.Host = 'www.yunpian.com'
    vf.ContentType = 'application/x-www-form-urlencoded'
    result_list = PhoneVerify.objects.filter(phone = phone)
    result = None
    if result_list.count() > 0:
        result = result_list[0]
        nowtime = datetime.datetime.utcnow()
        lasttime = result.update_time.replace(tzinfo=None)
        if (nowtime - lasttime) < datetime.timedelta(seconds=30):
            return False
    apikey = '72c9f01d5db2dc40f4aa31865b17940c'
    tplvalue = '#code#=' + content
    res = tpl_send_sms(apikey, '512797', tplvalue, phone)
    jsres = simplejson.loads(res)
    msg = jsres['code']
    print msg
    print result
    if str(msg) == '0':
        if result is not None:
            result.verify_code = content
            result.update_time = datetime.datetime.now()
            result.save()
        else:
            new_ver = PhoneVerify()
            new_ver.phone = phone
            new_ver.update_time = datetime.datetime.now()
            new_ver.verify_code = content
            new_ver.save()
        return True
    else:
        print jsres
        return False