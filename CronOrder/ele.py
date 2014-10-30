from bs4 import BeautifulSoup
from CronOrder.models import *
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

def catcheleorder(merid, cookielist):
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
    print dip
    a.Proxy = dip
    curmet = Merchant.objects.filter(id = merid)
    if curmet.count() == 0:
        return None
    auto_id = curmet[0].todaynum
    if cookielist is None:
        user = str(curmet[0].ele_account)
        passwd = str(curmet[0].ele_passwd)
        postdic = {'username': user, 'password': passwd}
        html = a.GetResFromRequest('POST', 'http://napos.ele.me/auth/doLogin', 'utf-8', postdic, use_proxy=True)
        print html
    # if 'success' not in html:
        time.sleep(2)
    else:
        a.CookieList = cookielist
    print a.CookieList
    html = a.GetResFromRequest('GET', 'http://napos.ele.me/dashboard/index/list/unprocessed_waimai', 'utf-8', use_proxy=True)
    soup = BeautifulSoup(html)
    intro = soup.find('ul', attrs={'id': 'list_items'})
    # print intro
    if intro is None:
        return None
    res = intro.findAll('li')
    for item in res:
        neworder = DayOrder()
        onpay = False
        detail = item.find('p', attrs={'class': 'list_addr'})
        price = item.find('p', attrs={'class': 'list_price'})
        menu = item.find('div', attrs={'class': 'menu_content'})
        orderid = item['orderid']
        ifhave = DayOrder.objects.filter(order_id_old = str(orderid))
        if ifhave.count() > 0:
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
        createqr(1, newid)
        auto_id += 1
        curmet[0].todaynum = auto_id
        curmet[0].save()
        address = detail.string
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
        neworder.platform = 2
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
