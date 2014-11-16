#coding: utf-8
import urllib
import re
import random
import urllib2
import cookielib
import hashlib
import datetime
from AlinLog.models import *
from bs4 import BeautifulSoup
from CronOrder.NetSpider import *
from ProxyWork.models import *

def getproxy():
    url = "http://cn-proxy.com/"
    a = NetSpider()
    a.Host = 'www.baidu.com'
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    s = soup.findAll('tr')
    # print len(s)
    newitems = 0
    for i in range(2, len(s)):
        try:
            speed = s[i].findAll('td')[3]
            speedres = speed.find('strong', attrs={'class': 'bar'})
            reres = re.findall(r'width[: ]+(\d{1,3})[%]', speedres['style'])
            if int(reres[0]) > 59:
                proxip = s[i].findAll('td')[0].string+':'+s[i].findAll('td')[1].string
                ishave = Proxy.objects.filter(ip = proxip)
                print proxip
                a.Proxy = proxip
                res = a.GetResFromRequest('GET', "http://www.baidu.com/", 'utf-8', use_proxy=True)
                if res is not None and ishave.count() == 0:
                    newitems += 1
                    newproxy = Proxy()
                    newproxy.ip = proxip
                    newproxy.is_online = True
                    newproxy.is_used = False
                    newproxy.get_time = datetime.datetime.now()
                    newproxy.save()
        except:
            continue
    content = '新增代理IP成功，新增数量' + str(newitems) + '条'
    print content
    newlog = CronLog()
    newlog.content = content
    newlog.ltype = 1
    newlog.status = True
    newlog.save()


def distriproxy(merid):
    ifbind = Proxy.objects.filter(bind_merchant = merid)
    if ifbind.count() > 0:
        return ifbind[0].ip
    can_proxy_list = Proxy.objects.filter(is_used = False, is_online = True)
    pronum = can_proxy_list.count()
    if pronum == 0:
        print 'no proxy ip availble'
        return None
    proxid = random.randint(1, pronum)
    proxy = can_proxy_list[(proxid-1)]
    proxy.bind_merchant = Merchant.objects.get(id = merid)
    proxy.is_used = True
    proxy.save()
    return proxy.ip

def delofflineproxy(ipstr):
    offline = Proxy.objects.filter(ip = str(ipstr))
    if offline.count() > 0:
        offline.delete()
    return True

def checkproxy():
    a = NetSpider()
    a.Host = 'www.baidu.com'
    useless = 0
    off = Proxy.objects.filter(is_online = False).delete()
    oters = Proxy.objects.all()
    print oters.count()
    for item in oters:
        a.Proxy = item.ip
        res = a.GetResFromRequest('GET', "http://www.baidu.com/", 'utf-8', use_proxy=True)
        if res is None:
            print 'del ' + item.ip
            item.delete()
            useless += 1
        else:
            print item.ip + ' connect success'
    content = '代理检验完成，删除无效代理' + str(useless) + '个'
    print content
    newlog = CronLog()
    newlog.ltype = 2
    newlog.content = content
    newlog.status = True
    newlog.save()
