# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from CronOrder.models import *
from CronOrder.endecy import *
import cookielib
from CronOrder.method import *
from QRcode.method import *
from CronOrder.NetProcess import *
from ProxyWork.method import *
from AlinLog.models import RunTimeLog
import datetime
import time
import simplejson
# http://napos.ele.me/order/processOrder/id/12259070287130497/category/1
# ttp://napos.ele.me/order/setInvalid/id/12459171300411697/category/1?type=6&remark=
class Ele(object):
    def __init__(self):
        self.net = NetProcess()
        # self.net.Host = 'napos.ele.me'

    def catcheorder(self, merchant):
        thiscount = 0
        # self.net.Referer = 'http://napos.ele.me/'
        print 'catcheele'
        # self.set_proxy(merchant)
        if not self.iflogin(merchant):
            res = self.loginele(merchant)
            if res is None or res is False:
                return None
        # cur_list = Merchant.objects.filter(id = self.merchantid)
        cache_list = CatcheData.objects.filter(merchant = merchant)
        cache = cache_list[0]
        self.net.SetCookie(str(cache.ele_cookie))
        tn = str(time.time())[0:10] + '000'
        requrl = 'http://napos.ele.me/order/list?list=unprocessed_waimai&t=' + tn
        html = self.net.GetResFromRequest('GET', requrl, 'utf-8')
        print html
        # with open('abc.txt', 'r') as f1:
        #     line = f1.readline()
        #     while line:
        #         html += line
        #         line = f1.readline()
        # print html
        if not isinstance(html, str):
            newlog = RunTimeLog()
            newlog.content = '爬虫抓单失败'
            newlog.err_message = str(html)
            newlog.status = False
            newlog.ltype = 18
            newlog.merchant = merchant
            newlog.save()
            # check_proxy_times(str(self.net.Proxy))
            return None
        # reset_proxy_times(str(self.net.Proxy))
        soup = BeautifulSoup(html)
        intro = soup.find('ul', attrs={'id': 'list_items'})
        if intro is None:
            notlogin = soup.find('label', attrs={'for': 'tab1'})
            if notlogin is not None:
                self.cookie = None
            print 'no new orders, login failed'
            return False
        res = intro.findAll('li')
        if len(res) == 0:
            print 'no new orders'
            return False
        thiscount = int(DayOrder.objects.filter(merchant=merchant, platform=2).count()) + 1
        # print 'start: ' + str(thiscount)
        for item in res:
            print item
            neworder = DayOrder()
            onpay = False
            yu_time = item.find('a', attrs={'rel': 'tipsy'})
            process_num = item.find('span', attrs={'class': 'process_num'})
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
            newid = createAlinOrderNum(2, merchant.id, thiscount)
            thiscount += 1
            qrres = createqr(1, newid)
            time.sleep(1)
            if yu_time.has_attr('explain'):
                res = re.findall(r'([0-9,:, ,-]+)', str(yu_time['explain']))
                if len(res) > 0:
                    yutt = time.strptime(str(res[0]), "%Y-%m-%d %H:%M:%S")
                    yudatetime = datetime.datetime(*yutt[:6])
                    neworder.send_time = yudatetime
                else:
                    neworder.send_time = datetimee
            else:
                neworder.send_time = datetimee
            address = detail.string[3:]
            neworder.address = address[1:]
            neworder.order_id_alin = newid
            neworder.order_id_old = orderid
            neworder.origin_price = price.string[1:]
            neworder.real_price = price.string[1:]
            orderphone = phone.string[3:]
            phonelist = orderphone.split(',')
            neworder.phone = phonelist[0]
            neworder.order_time = datetimee
            neworder.status = 1
            neworder.promotion = 'nothing'
            neworder.pay = onpay
            neworder.note = note
            if len(phonelist) > 1:
                neworder.note += '应急电话：%s' % phonelist[1]
            neworder.platform = 2
            neworder.qr_path = qrres
            neworder.merchant = merchant
            neworder.plat_num = str(process_num.string)
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
        return True


    def iflogin(self, merchant):
        cache_list = CatcheData.objects.filter(merchant = merchant)
        if cache_list.count() > 0:
            cache = cache_list[0]
            if cache.ele_cookie != '':
                return True
            return False
        else:
            return False

    def loginele(self, curmet):
        # self.set_proxy(curmet)
        # self.net.Referer = 'http://napos.ele.me/login'
        print 'loginele'
        user = str(curmet.ele_account)
        passwd = str(curmet.ele_passwd)
        de_pass = Decrypt(passwd)
        postdic = {'username': user, 'password': de_pass}
        # print 'login ele'
        html = self.net.GetResFromRequest('POST', 'http://napos.ele.me/auth/doLogin', 'utf-8', postdic)
        # print 'login end'
        if not isinstance(html, str):
            newlog = RunTimeLog()
            newlog.content = '饿了么登陆失败'
            newlog.merchant = curmet
            newlog.err_message = str(html)
            newlog.ltype = 15
            newlog.status = False
            newlog.save()
            # check_proxy_times(str(self.net.Proxy))
        else:
            # reset_proxy_times(str(self.net.Proxy))
            res_json = simplejson.loads(html)
            if res_json['success'] is False:
                errmsg = str(res_json['message']).decode('unicode_escape')
                curmet.ele_message = errmsg
                curmet.ele_status = False
                curmet.save()
                newlog = RunTimeLog()
                newlog.content = '饿了么登陆失败'
                newlog.merchant = curmet
                newlog.err_message = errmsg
                newlog.ltype = 15
                newlog.save()
                return False
            elif res_json['success'] is True:
                # if self.net.Cookies['SSID'] == 'nothing find':
                #     res = self.loginele()
                #     return res
                curmet.ele_status = True
                curmet.save()
                cache_list = CatcheData.objects.filter(merchant = curmet)
                print str(self.net.OutPutCookie())
                if cache_list.count() > 0:
                    cache = cache_list[0]
                    cache.ele_cookie = str(self.net.OutPutCookie())
                    cache.save()
                else:
                    cache = CatcheData()
                    cache.ele_cookie = str(self.net.OutPutCookie())
                    cache.merchant = curmet
                    cache.save()
                return True

    def ensureorder(self, curmet, order):
        # curmet_list = Merchant.objects.filter(id = self.merchantid)
        # if curmet_list.count() == 0:
        #     return None
        # self.set_proxy(curmet)
        if not self.iflogin(curmet):
            res = self.loginele(curmet)
            if res is None or res is False:
                return None
        cache_list = CatcheData.objects.filter(merchant = curmet)
        cache = cache_list[0]
        self.net.SetCookie(str(cache.ele_cookie))
        requrl = 'http://napos.ele.me/order/processOrder/id/' + str(order) + '/category/1'
        html = self.net.GetResFromRequest('GET', requrl, 'utf-8')
        if not isinstance(html, str):
            newlog = RunTimeLog()
            newlog.content = '确认饿了没订单失败'
            newlog.status = False
            newlog.err_message = str(html)
            newlog.ltype = 16
            newlog.merchant = curmet
            newlog.save()
            return False
        if str(html) == '0':
            newlog = RunTimeLog()
            newlog.content = '确认饿了没订单失败'
            newlog.status = False
            newlog.err_message = str(order) + html
            newlog.ltype = 16
            newlog.merchant = curmet
            newlog.save()
            return False
        return True

    def refuseorder(self, curmet, order):
        # self.set_proxy(curmet)
        if not self.iflogin(curmet):
            res = self.loginele(curmet)
            if res is None or res is False:
                return None
        cache_list = CatcheData.objects.filter(merchant = curmet)
        cache = cache_list[0]
        self.net.SetCookie(str(cache.ele_cookie))
        requrl = 'http://napos.ele.me/order/setInvalid/id/' + str(order) + '/category/1?type=6&remark='
        html = self.net.GetResFromRequest('GET', requrl, 'utf-8')
        if not isinstance(html, str):
            newlog = RunTimeLog()
            newlog.content = '拒绝饿了么订单失败'
            newlog.status = False
            newlog.err_message = str(html)
            newlog.ltype = 17
            newlog.merchant = curmet
            newlog.save()
            return False
        if str(html) == '0':
            newlog = RunTimeLog()
            newlog.content = '拒绝饿了么订单失败'
            newlog.ltype = 17
            newlog.err_message = str(order) + html
            newlog.status = False
            newlog.merchant = curmet
            newlog.save()
            return False
        return True
    #
    # def set_proxy(self, curmet):
    #     ip = distriproxy(str(curmet.id))
    #     # self.net.Proxy = str(ip)