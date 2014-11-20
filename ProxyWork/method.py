#coding: utf-8
import random
from AlinLog.models import *
from ProxyWork.models import *
from ProxyWork.proxys import *

def getproxy(args = None):
    a = NetSpider()
    a.Host = 'www.hao123.com'
    errmsg = ''
    myproxy = SProxy()
    ip_list = myproxy.renew_proxy()
    newitems = 0
    for item in ip_list:
        try:
            ishave = Proxy.objects.filter(ip = str(item))
            if ishave.count() > 0:
                continue
            a.Proxy = item
            res = a.GetResFromRequest('GET', "http://www.hao123.com/", 'utf-8', use_proxy=True)
            if res is not None:
                newitems += 1
                newproxy = Proxy()
                newproxy.ip = item
                newproxy.is_online = True
                newproxy.is_used = False
                newproxy.req_times = 0
                newproxy.get_time = datetime.datetime.now()
                newproxy.save()
        except Exception, e:
            print e
            errmsg = str(e)
            continue
    content = '新增代理IP成功，新增数量' + str(newitems) + '条'
    print content
    newlog = CronLog()
    newlog.content = content
    newlog.ltype = 1
    newlog.err_message = errmsg
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
    newlog = RunTimeLog()
    newlog.content = '获取代理IP:' + str(proxy.ip) + '成功'
    newlog.status = True
    newlog.ltype = 14
    newlog.merchant = Merchant.objects.get(id = merid)
    newlog.save()
    return proxy.ip

def delofflineproxy(ipstr):
    offline = Proxy.objects.filter(ip = str(ipstr))
    if offline.count() > 0:
        offline.delete()
    return True

def check_proxy_times(ipstr):
    times = Proxy.objects.filter(ip = str(ipstr))
    if times.count() > 0:
        time = times[0]
        if time.req_times == 3:
            delofflineproxy(ipstr)
        else:
            time.req_times += 1
            time.save()
        return True
    return False

def reset_proxy_times(ipstr):
    times = Proxy.objects.filter(ip = str(ipstr))
    if times.count() > 0:
        time = times[0]
        time.req_times = 0
        time.save()
    return True

def checkproxy(args = None):
    a = NetSpider()
    a.Host = 'napos.ele.me'
    useless = 0
    off = Proxy.objects.filter(is_online = False).delete()
    oters = Proxy.objects.all()
    print oters.count()
    for item in oters:
        a.Proxy = item.ip
        res = a.GetResFromRequest('GET', "http://napos.ele.me/login", 'utf-8', use_proxy=True)
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
