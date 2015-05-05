import random
import simplejson
import string
import datetime
import urllib
from AlinApi.models import *
from AlinApi.yunpian import *
from django.db.models.query import QuerySet
from AlinLog.error import except_handle
from CronOrder.NetSpider import *
from django.utils import timezone
from django.db import models
from django.core.paginator import Page
import string
import time
import xmltodict

def createverifycode(phone, count=6):
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


def isactive(lastactivetime, det=600):
    try:
        print lastactivetime
        nowt = datetime.datetime.utcnow()
        print nowt
        detla = nowt - lastactivetime
        if detla > datetime.timedelta(seconds=det):
            return False
        else:
            return True
    except Exception, e:
        except_handle(e)


def encodejson(status, body):
    tmpjson = {}
    tmpjson['status'] = status
    tmpjson['body'] = body
    return simplejson.dumps(tmpjson)

def createtoken(count = 32):
    return string.join(random.sample('ZYXWVUTSRQPONMLKJIHGFEDCBA1234567890zyxwvutsrqponmlkjihgfedcba+=', count)).replace(" ", "")


def string_to_datetime(timestring, timeformat='%Y-%m-%d'):
    dateres = datetime.datetime.strptime(timestring, timeformat)
    return dateres

def datetime_to_timestamp(datetimet):
    return time.mktime(datetimet.timetuple())

def datetime_to_string(datetimet):
    return str(timezone.localtime(datetimet))


def model_serializer(djmodels, datetime_format='timestamp', serializer='dict', include_attr=None,  except_attr=None, deep=False):
    if djmodels is None:
        return None
    if datetime_format == 'timestamp':
        time_format_func = datetime_to_timestamp
    elif datetime_format == 'string':
        time_format_func = datetime_to_string
    else:
        time_format_func = datetime_to_timestamp
    result = []
    if isinstance(djmodels, models.Model):
        djmodels = [djmodels]
    if isinstance(djmodels, (QuerySet, list, Page)):
        for itm in djmodels:
            attr_list = itm.serializer(deep)
            if '_state' in attr_list:
                attr_list.pop('_state')
            if include_attr is not None:
                new_attr_list = {}
                for i in include_attr:
                    try:
                        new_attr_list[i] = attr_list[i]
                    except Exception, e:
                        print 'no include attr' + str(e)
                        continue
                attr_list = new_attr_list
            datetime_list = [i for i in attr_list.items() if isinstance(i[1], datetime.datetime)]
            if len(datetime_list) > 0:
                for i in datetime_list:
                    attr_list[i[0]] = time_format_func(i[1])
            if except_attr is not None:
                for i in except_attr:
                    try:
                        attr_list.pop(i)
                    except Exception, e:
                        print 'no except attr' + str(e)
                        continue
            if isinstance(djmodels, list):
                result = attr_list
                break
            else:
                result.append(copy.copy(attr_list))
    if serializer == 'json':
        return simplejson.dumps(result)
    elif serializer == 'dict':
        return result
    elif serializer == 'xml':
        dd = {'xmlobj': result}
        return xmltodict.unparse(dd)
    return None
