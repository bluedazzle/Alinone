# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from CronOrder.models import *
from CronOrder.endecy import *
import cookielib
from CronOrder.method import *
from QRcode.method import *
from CronOrder.NetSpider import *
from ProxyWork.method import *
import datetime
import time
import simplejson
# http://napos.ele.me/order/processOrder/id/12259070287130497/category/1
# ttp://napos.ele.me/order/setInvalid/id/12459171300411697/category/1?type=6&remark=
class Ele(object):
    def __init__(self, merchantid):
        self.account = ''
        self.password = ''
        self.merchantid = merchantid
        self.cookie = None
        self.net = NetSpider()
        self.net.Host = 'napos.ele.me'

    def catcheorder(self):
        curmet = None
        thiscount = 0
        self.net.Referer = 'http://napos.ele.me/'
        if not self.iflogin():
            res = self.loginele()
            if res is None or res is False:
                return None
        html = self.net.GetResFromRequest('GET', 'http://napos.ele.me/dashboard/index/list/unprocessed_waimai', 'utf-8', use_proxy=True)
        # # print html
        # html = ''
        # with open('abc.txt', 'r') as f1:
        #     line = f1.readline()
        #     while line:
        #         html += line
        #         line = f1.readline()
        if html is None:
            return None
        soup = BeautifulSoup(html)
        intro = soup.find('ul', attrs={'id': 'list_items'})
        if intro is None:
            print 'no new orders'
            return False
        cur_list = Merchant.objects.filter(id = self.merchantid)
        if cur_list.count() == 0:
            return None
        curmet = cur_list[0]
        res = intro.findAll('li')
        if len(res) == 0:
            print 'no new orders'
            return False
        thiscount = curmet.todaynum
        # print 'start: ' + str(thiscount)
        for item in res:
            neworder = DayOrder()
            onpay = False
            detail = item.find('p', attrs={'class': 'list_addr'})
            note = item.find('p', attrs={'class': 'list_description'})
            price = item.find('p', attrs={'class': 'list_price'})
            menu = item.find('div', attrs={'class': 'menu_content'})
            orderid = item['orderid']
            print orderid
            ifhave = DayOrder.objects.filter(order_id_old = str(orderid))
            if ifhave.count() > 0:
            # print 'break'
            # print auto_id + 1
                continue
            timestamp = item['createdat']
            online = item['online-pay']
            if note is not None:
                note = note.string[2:]
            if online != '':
                onpay = True
            phone = item.find('p', attrs={'class': 'list_customer'})
            formattime = time.localtime(float(timestamp))
            datetimee = datetime.datetime(*formattime[:6])
            timee = time.strftime('%Y-%m-%d %H:%M:%S', formattime)
            newid = createAlinOrderNum(2, self.merchantid, thiscount)
            thiscount += 1
            qrres = createqr(1, newid)
            address = detail.string[3:]
            neworder.address = address[1:]
            neworder.order_id_alin = newid
            neworder.order_id_old = orderid
            neworder.origin_price = price.string[1:]
            neworder.real_price = price.string[1:]
            neworder.phone = phone.string[3:]
            neworder.order_time = datetimee
            neworder.send_time = datetimee
            neworder.status = 1
            neworder.promotion = 'nothing'
            neworder.pay = onpay
            neworder.note = note
            neworder.platform = 2
            neworder.qr_path = qrres
            neworder.merchant = curmet
            neworder.save()
            print timee
            print orderid
            print phone.string[3:]
            print price.string[1:]
            print address
            dishname = menu.findAll(attrs = {'class': 'dishname'})
            dishcount = menu.findAll(attrs = {'class': 'item_quantity'})
            dishprice = menu.findAll(attrs = {'class': 'item_price'})
            for i in range(0, len(dishname)):
                newdish = Dish()
                newdish.dish_name = str(dishname[i].string)
                newdish.dish_count = int(dishcount[i].string)
                newdish.dish_price = float(dishprice[i].string)
                newdish.order = DayOrder.objects.get(order_id_alin = newid)
                newdish.save()
        return thiscount


    def iflogin(self):
        if self.cookie is None:
            return False
        else:
            return True

    def loginele(self):
        self.net.Referer = 'http://napos.ele.me/login'
        dip = distriproxy(self.merchantid)
        if dip is None:
            return None
        self.net.Proxy = dip
        curmet_list = Merchant.objects.filter(id = self.merchantid)
        if curmet_list.count() == 0:
            print 'no mer'
            return None
        curmet = curmet_list[0]
        user = str(curmet.ele_account)
        passwd = str(curmet.ele_passwd)
        de_pass = Decrypt(passwd)
        postdic = {'username': user, 'password': de_pass}
        # print postdic
        self.account = user
        self.password = de_pass
        html = self.net.GetResFromRequest('POST', 'http://napos.ele.me/auth/doLogin', 'utf-8', postdic, use_proxy=True)
        if html is None:
            delofflineproxy(self.net.Proxy)
            res = self.loginele()
            return res
        else:
            res_json = simplejson.loads(html)
            if res_json['success'] is False:
                errmsg = str(res_json['message']).decode('unicode_escape')
                curmet.ele_message = errmsg
                curmet.ele_status = False
                curmet.save()
                print 'fail'
                return False
            elif res_json['success'] is True:
                if self.net.SearchCookie('SSID') == 'nothing find':
                    res = self.loginele()
                    return res
                curmet.ele_status = True
                curmet.save()
                self.cookie = self.net.CookieList
                print self.cookie
                print 'succ'
                return True

    def ensureorder(self, orderlist):
        faillist = ''
        curmet_list = Merchant.objects.filter(id = merid)
        if curmet_list.count() == 0:
            return None
        curmet = curmet_list[0]
        if not self.iflogin():
            res = self.loginele()
            if res is None or res is False:
                return None
        for itm in orderlist:
            requrl = 'http://napos.ele.me/order/processOrder/id/' + str(itm) + '/category/1'
            html = self.net.GetResFromRequest('GET', requrl, 'utf-8', use_proxy=True)
            print html
            if str(html) == '0':
                faillist += str(itm)
                faillist += ','
        if faillist != '':
            if curmet.faillist is None:
                curmet.faillist = faillist
            else:
                curmet.faillist += faillist
            curmet.save()
            return False
        return True

    def refuseorder(self):
        curmet_list = Merchant.objects.filter(id = merid)
        if curmet_list.count() == 0:
            return None
        curmet = curmet_list[0]
        if not self.iflogin():
            res = self.loginele()
            if res is None or res is False:
                return None
        for itm in orderlist:
            requrl = 'http://napos.ele.me/order/setInvalid/id/' + str(itm) + '/category/1?type=6&remark='
            html = self.net.GetResFromRequest('GET', requrl, 'utf-8', use_proxy=True)
            print html
            if str(html) == '0':
                return False
        #         faillist += str(itm)
        #         faillist += ','
        # if faillist != '':
        #     if curmet.faillist is None:
        #         curmet.faillist = faillist
        #     else:
        #         curmet.faillist += faillist
        #     curmet.save()
        #     return False
        return True