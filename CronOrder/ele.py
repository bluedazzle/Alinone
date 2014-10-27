from bs4 import BeautifulSoup
from CronOrder.models import *
from CronOrder.method import *
from QRcode.method import *
import datetime
import time
import sys


def catcheleorder(merid, autoid):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    html = ''
    with open('abc.txt', 'r') as f1:
        line = f1.readline()
        while line:
            html += line
            line = f1.readline()
        f1.close()
    soup = BeautifulSoup(html)
    intro = soup.findAll('ul', attrs={'id': 'list_items'})
    newid = createAlinOrderNum(2, merid, autoid)
    createqr(1, newid)
    for item in intro:
        neworder = DayOrder()
        onpay = False
        res = item.find('li', attrs={'class': 'new'})
        detail = item.find('p', attrs={'class': 'list_addr'})
        price = item.find('p', attrs={'class': 'list_price'})
        menu = item.find('div', attrs={'class': 'menu_content'})
        orderid = res['orderid']
        timestamp = res['createdat']
        online = res['online-pay']
        if online != '':
            onpay = True
        phone = item.find('p', attrs={'class': 'list_customer'})
        formattime = time.localtime(float(timestamp))
        datetimee = datetime.datetime(*formattime[:6])
        timee = time.strftime('%Y-%m-%d %H:%M:%S', formattime)
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
        # print timee
        # print orderid
        # print phone.string[3:]
        # print price.string[1:]
        # print address
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
    return 'success'
