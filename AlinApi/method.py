import random
import simplejson
import string
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
    postdic = {}
    apikey = '72c9f01d5db2dc40f4aa31865b17940c'
    postdic['mobile'] = phone
    postdic['apikey'] = apikey
    postdic['tpl_id'] = '512797'
    postdic['tpl_value'] = '#code#=' + content
    res = vf.GetResFromRequest('POST', 'http://yunpian.com/v1/sms/tpl_send.json', 'UTF-8', postdic)
    jsres = simplejson.loads(res)
    msg = jsres['code']
    if str(msg) == '0':
        return True
    else:
        print jsres
        return False
