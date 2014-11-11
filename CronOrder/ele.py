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
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# http://napos.ele.me/order/processOrder/id/12259070287130497/category/1
# ttp://napos.ele.me/order/setInvalid/id/12459171300411697/category/1?type=6&remark=
class Ele(object):
    def __init__(self):
        self.account = ''
        self.password = ''
        self.merchantid = ''
        self.cookie = None

    def catchorder(self):
        return 0


def ensureleeorder(merid, orderlist):
    faillist = ''
    e = NetSpider()
    e.Host = 'napos.ele.me'
    e.Referer = 'http://napos.ele.me/login'
    dip = distriproxy(merid)
    if dip is None:
        return None
    e.Proxy = dip
    curmet_list = Merchant.objects.filter(id = merid)
    if curmet_list.count() == 0:
        return None
    curmet = curmet_list[0]
    user = str(curmet.ele_account)
    passwd = str(curmet.ele_passwd)
    de_pass = Decrypt(passwd)
    postdic = {'username': user, 'password': de_pass}
    html = e.GetResFromRequest('POST', 'http://napos.ele.me/auth/doLogin', 'utf-8', postdic, use_proxy=True)
    if html is None:
        delofflineproxy(e.Proxy)
        renewres = ensureleeorder(merid)
        if renewres is not None:
            return renewres
        else:
            return None
    else:
        res_json = simplejson.loads(html)
        if res_json['success'] == 'false':
            errmsg = str(res_json['message']).decode('unicode_escape')
            curmet.ele_message = errmsg
            curmet.ele_status = False
            curmet.save()
            return None
        elif res_json['success'] == 'true':
            curmet.ele_status = True
            curmet.save()
    for itm in orderlist:
        requrl = 'http://napos.ele.me/order/processOrder/id/' + str(itm) + '/category/1'
        html = e.GetResFromRequest('GET', requrl, 'utf-8', use_proxy=True)
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





def catcheleorder(merid, cookielist=None):
    auto_id = 0
    html = ''
    # with open('abc.txt', 'r') as f1:
    #     line = f1.readline()
    #     while line:
    #         html += line
    #         line = f1.readline()
    #     f1.close()
    a = NetSpider()
    # http://napos.ele.me/auth/doLogin
    a.Host = 'napos.ele.me'
    a.Referer = 'http://napos.ele.me/login'
    dip = distriproxy(merid)
    if dip is None:
        return None
    print dip
    a.Proxy = dip
    curmet_list = Merchant.objects.filter(id = merid)
    if curmet_list.count() == 0:
        return None
    curmet = curmet_list[0]
    auto_id = curmet.todaynum
    if cookielist is None:
        user = str(curmet.ele_account)
        passwd = str(curmet.ele_passwd)
        de_pass = Decrypt(passwd)
        postdic = {'username': user, 'password': de_pass}
        html = a.GetResFromRequest('POST', 'http://napos.ele.me/auth/doLogin', 'utf-8', postdic, use_proxy=True)
        if html is None:
            delofflineproxy(a.Proxy)
            renewres = catcheleorder(merid)
            if renewres is not None:
                return renewres
            else:
                return None
        else:
            res_json = simplejson.loads(html)
            if res_json['success'] == 'false':
                errmsg = str(res_json['message']).decode('unicode_escape')
                curmet.ele_message = errmsg
                curmet.ele_status = False
                curmet.save()
                return None
            elif res_json['success'] == 'true':
                curmet.ele_status = True
                curmet.save()
    else:
        a.CookieList = cookielist
    print a.CookieList
    html = a.GetResFromRequest('GET', 'http://napos.ele.me/dashboard/index/list/unprocessed_waimai', 'utf-8', use_proxy=True)
    if html is None:
        return None
    soup = BeautifulSoup(html)
    intro = soup.find('ul', attrs={'id': 'list_items'})
    if intro is None:
        return None
    res = intro.findAll('li')
    for item in res:
        neworder = DayOrder()
        onpay = False
        detail = item.find('p', attrs={'class': 'list_addr'})
        note = item.find('p', attrs={'class': 'list_description'})
        price = item.find('p', attrs={'class': 'list_price'})
        menu = item.find('div', attrs={'class': 'menu_content'})
        orderid = item['orderid']
        ifhave = DayOrder.objects.filter(order_id_old = str(orderid))
        if ifhave.count() > 0:
            # print 'break'
            # print auto_id + 1
            continue
        timestamp = item['createdat']
        online = item['online-pay']
        if online != '':
            onpay = True
        phone = item.find('p', attrs={'class': 'list_customer'})
        formattime = time.localtime(float(timestamp))
        datetimee = datetime.datetime(*formattime[:6])
        timee = time.strftime('%Y-%m-%d %H:%M:%S', formattime)
        newid = createAlinOrderNum(2, merid, auto_id)
        qrres = createqr(1, newid)
        curmet.todaynum += 1
        print curmet.todaynum
        curmet.save()
        address = detail.string[3:]
        neworder.address = address
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
        neworder.merchant = Merchant.objects.get(id = merid)
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
    return a.CookieList
