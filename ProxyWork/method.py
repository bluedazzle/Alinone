#coding: utf-8
import urllib
import re
import random
import urllib2
import cookielib
import hashlib
import datetime
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
                    newproxy = Proxy()
                    newproxy.ip = proxip
                    newproxy.is_online = True
                    newproxy.is_used = False
                    newproxy.get_time = datetime.datetime.now()
                    newproxy.save()
        except:
            continue

def distriproxy(merid):
    ifbind = Proxy.objects.filter(bind_merchant = merid)
    if ifbind.count() > 0:
        return ifbind[0].ip
    can_proxy_list = Proxy.objects.filter(is_used = False, is_online = True)
    pronum = can_proxy_list.count()
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
