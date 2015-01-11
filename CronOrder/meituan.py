# -*- coding: utf-8 -*-
from CronOrder.endecy import *
import cookielib
from CronOrder.method import *
from QRcode.method import *
from CronOrder.NetSpider import *
from ProxyWork.method import *
from AlinLog.models import RunTimeLog
import datetime
import time
import simplejson


class Mei(object):
    def __init__(self):
        self.net = NetSpider()
        self.net.Host = 'waimaieapi.meituan.com'
        self.net.UserAgent = 'Dalvik/1.6.0 (Linux; U; Android 4.1.1; MI 2S MIUI/4.11.7)'
        self.net.ContentType = 'application/x-www-form-urlencoded'

    def get_token(self, curmet):
        user = str(curmet.mei_account)
        passwd = str(curmet.mei_passwd)
        de_pass = Decrypt(passwd)
        cache_list = CatcheData.objects.filter(merchant = curmet)
        sid = None
        verify_code = ''
        if cache_list.count() > 0:
            sid = cache_list[0].mei_sid
            if cache_list[0].mei_need_verify is True:
                if cache_list[0].mei_verify is not None:
                    verify_code = cache_list[0].mei_verify
                else:
                    return None
        sid = createMeiId()
        postdic = {'utm_medium': 'android',
                   'sid': sid,
                   'dVersion': '16_4.1.1',
                   'utm_source': '1',
                   'utm_content': '863077020776914',
                   'appName': '美团外卖商家版',
                   'dType': 'MI 2S',
                   'appCode': '41',
                   'validCode': verify_code,
                   'uuid': sid,
                   'utm_term': '2.1.6',
                   'appType': '4',
                   'logType': 'C',
                    'userName': user,
                   'password': de_pass}
        html = self.net.GetResFromRequest('POST', 'http://waimaieapi.meituan.com/api/poi/logon/app/v4', 'utf-8', postdic)
        if not isinstance(html, str):
            newlog = RunTimeLog()
            newlog.content = '美团服务器未返回响应'
            newlog.status = False
            newlog.err_message = str(html)
            newlog.ltype = 30
            newlog.merchant = curmet
            newlog.save()
            return None
        res_json = simplejson.loads(html)
        login_status = str(res_json['code'])
        login_msg = str(res_json['msg'])
        if login_msg != 'ok' or login_status != '0':
            if cache_list.count() == 0:
                newcache = CatcheData()
                newcache.merchant = curmet
                newcache.mei_sid = str(sid)
                newcache.save()
            curmet.mei_message = login_msg
            curmet.mei_status = False
            curmet.save()
            newlog = RunTimeLog()
            newlog.content = '美团登陆失败'
            newlog.merchant = curmet
            newlog.err_message = html
            newlog.ltype = 31
            newlog.save()
            self.errhandle(login_status, curmet)
            return False
        login_data = res_json['data']
        if cache_list.count > 0:
            cache = cache_list[0]
            cache.mei_token = str(login_data['accessToken'])
            cache.mei_acctid = str(login_data['acctId'])
            cache.mei_sid = str(sid)
            cache.mei_need_verify = False
            cache.mei_verify = ''
            poidata = login_data['poiLists'][0]
            cache.mei_id = str(poidata['id'])
            cache.mei_lastorderid = createMeiOrder(str(poidata['id']))
            print 'mei login'
            cache.save()
        else:
            cache = CatcheData()
            cache.merchant = curmet
            cache.mei_sid = str(sid)
            cache.mei_token = str(login_data['accessToken'])
            cache.mei_acctid = str(login_data['acctId'])
            poidata = login_data['poiLists'][0]
            cache.mei_id = str(poidata['id'])
            cache.mei_lastorderid = createMeiOrder(str(poidata['id']))
            cache.save()
        curmet.mei_status = True
        curmet.save()
        return True

    def getOrder(self, curmet):
        print 'getOrder'
        cache = None
        cache_list = CatcheData.objects.filter(merchant = curmet)
        if cache_list.count > 0:
            if cache_list[0].mei_token == '' or cache_list[0].mei_token is None:
                res = self.get_token(curmet)
                if res is False:
                    return None
                cache_list = CatcheData.objects.filter(merchant = curmet)
        cache = cache_list[0]
        postdic = {'utm_medium': 'android',
                   'wmPoiId': cache.mei_id,
                   'dVersion': '16_4.1.1',
                   'utm_source': '1',
                   'utm_content': '863077020776914',
                   'appName': '美团外卖商家版',
                   'dType': 'MI 2S',
                   'appCode': '41',
                   'uuid': cache.mei_sid,
                   'lastOrderId': cache.mei_lastorderid,
                   'utm_term': '2.1.6',
                   'appType': '4',
                   'logType': 'C',
                    'acctId': cache.mei_acctid,
                   'token': cache.mei_token}
        html = self.net.GetResFromRequest('POST', 'http://waimaieapi.meituan.com/api/order/new/orderList/v3', 'utf-8', postdic)
        if not isinstance(html, str):
            newlog = RunTimeLog()
            newlog.content = '美团服务器未返回响应'
            newlog.status = False
            newlog.err_message = str(html)
            newlog.ltype = 30
            newlog.merchant = curmet
            newlog.save()
            return None
        res_json = simplejson.loads(html)
        res_code = str(res_json['code'])
        res_msg = str(res_json['msg'])
        if res_code != '0':
            curmet.mei_message = res_msg
            curmet.mei_status = False
            curmet.save()
            newlog = RunTimeLog()
            newlog.content = '美团抓单失败'
            newlog.merchant = None
            newlog.err_message = html
            newlog.ltype = 32
            newlog.save()
            self.errhandle(res_code, curmet)
            return False
        res_data = res_json['data']
        thiscount = int(DayOrder.objects.filter(merchant=curmet, platform=3).count()) + 1
        for itm in res_data:
            mei_order_id = str(itm['wm_order_id_view'])
            ifhave = DayOrder.objects.filter(order_id_old = str(mei_order_id))
            if ifhave.count() > 0:
                continue
            onpay = False
            pay_status = str(itm['pay_status'])
            if pay_status != '0':
                onpay = True
            newdayorder = DayOrder()
            newid = createAlinOrderNum(3, curmet.id, thiscount)
            newdayorder.order_id_alin = newid
            newdayorder.qr_path = createqr(1, newid)
            newdayorder.address = str(itm['recipient_address'])
            newdayorder.phone = str(itm['recipient_phone'])
            newdayorder.real_price = str(itm['total_after'])
            newdayorder.send_time = timestampToDatetime(str(itm['delivery_btime']))
            newdayorder.order_time = timestampToDatetime(str(itm['order_time']))
            newdayorder.order_id_old = str(itm['wm_order_id_view'])
            newdayorder.note = str(itm['remark'])
            newdayorder.merchant = curmet
            newdayorder.status = 1
            newdayorder.platform = 3
            newdayorder.plat_num = str(itm['wm_poi_order_dayseq'])
            newdayorder.origin_price = str(itm['total_before'])
            newdayorder.pay = onpay
            newdayorder.save()
            dish_list = itm['details']
            for item in dish_list:
                newdish = Dish()
                newdish.dish_name = str(item['food_name'])
                newdish.dish_count = str(item['count'])
                newdish.dish_price = str(item['food_price'])
                newdish.order = DayOrder.objects.get(order_id_alin = newid)
                newdish.save()
            thiscount += 1
        curmet.mei_status = True
        curmet.save()
        return True

    def ensureOrder(self, curmet, orderid):
        cache_list = CatcheData.objects.filter(merchant = curmet)
        cache = None
        if cache_list.count > 0:
            if cache_list[0].mei_token == '':
                self.get_token(curmet)
                cache_list = CatcheData.objects.filter(merchant = curmet)
        cache = cache_list[0]
        postdic = {'utm_medium': 'android',
                   'wmPoiId': cache.mei_id,
                   'dVersion': '16_4.1.1',
                   'utm_source': '1',
                   'utm_content': '863077020776914',
                   'appName': '美团外卖商家版',
                   'dType': 'MI 2S',
                   'appCode': '41',
                   'uuid': cache.mei_sid,
                   'orderId': str(orderid),
                   'utm_term': '2.1.6',
                   'appType': '4',
                   'logType': 'C',
                    'acctId': cache.mei_acctid,
                   'token': cache.mei_token}
        html = self.net.GetResFromRequest('POST', 'http://waimaieapi.meituan.com/api/order/confirm/v3', 'utf-8', postdic)
        print html
        if not isinstance(html, str):
            newlog = RunTimeLog()
            newlog.content = '美团服务器未返回响应'
            newlog.status = False
            newlog.err_message = str(html)
            newlog.ltype = 30
            newlog.merchant = curmet
            newlog.save()
            return None
        res_json = simplejson.loads(html)
        res_code = str(res_json['code'])
        res_msg = str(res_json['msg'])
        if res_code != '0':
            curmet.mei_message = res_msg
            curmet.save()
            newlog = RunTimeLog()
            newlog.content = '美团接受订单失败'
            newlog.merchant = None
            newlog.err_message = html
            newlog.ltype = 33
            newlog.save()
            return self.errhandle(res_code, curmet)
        return True

    def refuseOrder(self, curmet, orderid):
        cache_list = CatcheData.objects.filter(merchant = curmet)
        cache = None
        if cache_list.count > 0:
            if cache_list[0].mei_token == '':
                self.get_token(curmet)
                cache_list = CatcheData.objects.filter(merchant = curmet)
        cache = cache_list[0]
        postdic = {'utm_medium': 'android',
                   'wmPoiId': cache.mei_id,
                   'dVersion': '16_4.1.1',
                   'utm_source': '1',
                   'utm_content': '863077020776914',
                   'appName': '美团外卖商家版',
                   'dType': 'MI 2S',
                   'appCode': '41',
                   'reasonId': '338',
                   'uuid': cache.mei_sid,
                   'orderId': str(orderid),
                   'utm_term': '2.1.6',
                   'appType': '4',
                   'logType': 'C',
                   'remark': '美食已售完',
                    'acctId': cache.mei_acctid,
                   'token': cache.mei_token}
        html = self.net.GetResFromRequest('POST', 'http://waimaieapi.meituan.com/api/order/cancel/v3', 'utf-8', postdic)
        if not isinstance(html, str):
            newlog = RunTimeLog()
            newlog.content = '美团服务器未返回响应'
            newlog.status = False
            newlog.err_message = str(html)
            newlog.ltype = 30
            newlog.merchant = curmet
            newlog.save()
            return None
        res_json = simplejson.loads(html)
        res_code = str(res_json['code'])
        res_msg = str(res_json['msg'])
        if res_code != '0':
            curmet.mei_message = res_msg
            curmet.save()
            newlog = RunTimeLog()
            newlog.content = '美团拒绝订单失败'
            newlog.merchant = curmet
            newlog.err_message = html
            newlog.ltype = 33
            newlog.save()
            return self.errhandle(res_code, curmet)
        return True

    def getVerify(self, curmet):
        cache_list = CatcheData.objects.filter(merchant = curmet)
        cache = cache_list[0]
        phone = curmet.alin_account
        print phone
        postdic = {'utm_medium': 'android',
                   'dVersion': '16_4.1.1',
                   'utm_source': '1',
                   'sid': cache.mei_sid,
                   'uuid': cache.mei_sid,
                   'utm_content': '863077020776914',
                   'appName': '美团外卖商家版',
                   'phone': phone,
                   'dType': 'MI 2S',
                   'appCode': '41',
                   'utm_term': '2.1.6',
                   'appType': '4',
                   'logType': 'C'}
        html = self.net.GetResFromRequest('POST', 'http://waimaieapi.meituan.com/api/poi/getValidCode', 'utf-8', postdic)
        print 'verfiy code'
        print html
        if not isinstance(html, str):
            newlog = RunTimeLog()
            newlog.content = '美团服务器未返回响应'
            newlog.status = False
            newlog.err_message = str(html)
            newlog.ltype = 30
            newlog.merchant = curmet
            newlog.save()
            return None
        res_json = simplejson.loads(html)
        res_code = str(res_json['code'])
        res_msg = str(res_json['msg'])
        if res_code != '0':
            curmet.mei_message = res_msg
            curmet.save()
            newlog = RunTimeLog()
            newlog.content = '美团验证码接收失败'
            newlog.merchant = curmet
            newlog.err_message = html
            newlog.ltype = 33
            newlog.save()
            return self.errhandle(res_code, curmet)
        return True



    def errhandle(self, errcode, curmet):
        if str(errcode) == '1001':
            self.get_token(curmet)
        elif str(errcode) == '2001':
            return 'c cancel'
        elif str(errcode) == '1012':
            cache = CatcheData.objects.filter(merchant = curmet)[0]
            cache.mei_need_verify = True
            self.getVerify(curmet)
            cache.save()
            return 'v need'
        else:
            return False
