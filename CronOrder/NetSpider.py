# -*- coding: utf-8 -*-
import cookielib
import urllib2
import urllib
import simplejson
import copy

class NetSpider(object):
    """docstring for NetSpider"""
    def __init__(self):
        self.__mainurl = ""
        self.__host = ""
        self.__referer = ""
        self.__proxy = ""
        self.__proxymethod = "http"
        self.__accept = "text/html, application/xhtml+xml, */*"
        self.__origin = ""
        self.__contenttype = "application/x-www-form-urlencoded"
        self.__useragent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36"
        self.__cookielist = cookielib.CookieJar()
        self.__postHeaders = {'Host':self.__host,
                            'Accept':self.__accept,
                            # 'Accept-Encoding':'gzip,deflate,sdch',
                            'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
                            'Cache-Control':'max-age=0',
                            'Connection':'keep-alive',
                            'Origin':self.__origin,
                            'Referer':self.__referer,
                            'Content-Type':self.__contenttype,
                            'User-Agent':self.__useragent}

    """property"""
    def getMainUrl(self): return self.__mainurl
    def setMainUrl(self, value):self.__mainurl = value
    MainUrl = property(getMainUrl, setMainUrl, "Property MainUrl")

    def getProxyMethod(self): return self.__proxymethod
    def setProxyMethod(self, value):
        self.__proxymethod = value
    ProxyMethod = property(getProxyMethod, setProxyMethod, "Property ProxyMethod")

    def getProxy(self): return self.__proxy
    def setProxy(self, value):
        self.__proxy = value
    Proxy = property(getProxy, setProxy, "Property Proxy")

    def getOrigin(self): return self.__origin
    def setOrigin(self, value):
        self.__postHeaders['Origin'] = value
        self.__origin = value
    Origin = property(getOrigin, setOrigin, "Property Origin")

    def getHost(self): return self.__host
    def setHost(self, value):
        self.__host = value
        self.__postHeaders['Host'] = value
    Host = property(getHost, setHost, "Property Host")

    def getReferer(self): return self.__referer
    def setReferer(self, value):
        self.__referer = value
        self.__postHeaders['Referer'] = value
    Referer = property(getReferer, setReferer, "Property Referer")

    def getAccept(self): return self.__accept
    def setAccept(self, value):
        self.__accept = value
        self.__postHeaders['Accept'] = value
    Accept = property(getAccept, setAccept, "Property Accept")

    def getContentType(self): return self.__contenttype
    def setContentType(self, value):
        self.__contenttype = value
        self.__postHeaders['Content-Type'] = value
    ContentType = property(getContentType, setContentType, "Property ContentType")

    def getUserAgent(self): return self.__useragent
    def setUserAgent(self, value):
        self.__useragent = value
        self.__postHeaders['User-Agent'] = value
    UserAgent = property(getUserAgent, setUserAgent, "Property UserAgent")

    def getCookieList(self): return self.__cookielist
    def setCookieList(self, value):self.__cookielist = value
    CookieList = property(getCookieList, setCookieList, "Property CookieList")

    def getPostHeaders(self): return self.__postHeaders
    def setPostHeaders(self, value): self.__postHeaders = value
    PostHeaders = property(getPostHeaders, setPostHeaders, "Property PostHeaders")

    """private_propety"""
    def __ErrorHandle(self,errtype):
        print errtype


    """method"""
    def GetResFromRequest(self,method,requrl,encodemethod = 'gbk',postDict = {''},reqdata = '',use_proxy = False):
        try:
            if use_proxy:
                proxy = {self.__proxymethod: self.__proxy}
                proxy_support = urllib2.ProxyHandler(proxy)
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.__cookielist), proxy_support)
            else:
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.__cookielist))
            urllib2.install_opener(opener)
            # req = urllib2.urlopen(requrl)
            req = None
            if method == 'POST':
                if reqdata != '':
                    req = urllib2.Request(requrl, reqdata)
                else:
                    postData = urllib.urlencode(postDict).encode()
                    req = urllib2.Request(requrl, postData)
                    # print req
            elif method == "GET":
                # print requrl
                req = urllib2.Request(requrl)
            for key, itm in self.__postHeaders.items():
                req.add_header(key, itm)
            res = urllib2.urlopen(req, timeout=6)
            try:
                resdata = res.read().decode(encodemethod)
                res.close()
                return str(resdata)
            except Exception, e:
                res.close()
                return e
        except Exception, e:
            self.__ErrorHandle(e)
            return e
        finally:
            pass


    def SearchCookie(self,searchkey):
        for index, cookie in enumerate(self.__cookielist):
            if(cookie.name == searchkey):
                return cookie.value
        return 'nothing find'

    def ShowCurrentCookie(self):
        if len(self.__cookielist) == 0:
            print "no cookie"
            return 0
        for index, cookie in enumerate(self.__cookielist):
            print index
            print str(cookie.name) + ' : ' + str(cookie.value)

    def OutPutCookie(self):
        if len(self.__cookielist) == 0:
            print "no cookie"
            return None
        outlist = []
        for cookie in self.__cookielist:
            newcookiedict = {}
            newcookiedict['name'] = cookie.name
            newcookiedict['version'] = cookie.version
            newcookiedict['value'] = cookie.value
            newcookiedict['port'] = cookie.port
            newcookiedict['port_specified'] = cookie.port_specified
            newcookiedict['domain'] = cookie.domain
            newcookiedict['domain_specified'] = cookie.domain_specified
            newcookiedict['domain_initial_dot'] = cookie.domain_initial_dot
            newcookiedict['path'] = cookie.path
            newcookiedict['path_specified'] = cookie.path_specified
            newcookiedict['secure'] = cookie.secure
            newcookiedict['expires'] = cookie.expires
            newcookiedict['discard'] = cookie.discard
            newcookiedict['comment'] = cookie.comment
            newcookiedict['comment_url'] = cookie.comment_url
            outlist.append(copy.copy(newcookiedict))
        return simplejson.dumps(outlist)

    def SetCookie(self, cookielist):
        cookie_list = simplejson.loads(cookielist)
        for itm in cookie_list:
            newcookie = cookielib.Cookie(None, None, None, None, None, itm['domain'], None, None, None, None, None, None, None, None, None, None)
            newcookie.version = itm['version']
            newcookie.name = itm['name']
            newcookie.value = itm['value']
            newcookie.port = itm['port']
            newcookie.port_specified = itm['port_specified']
            newcookie.domain_initial_dot = itm['domain_initial_dot']
            newcookie.domain_specified = itm['domain_specified']
            newcookie.path = itm['path']
            newcookie.path_specified = itm['path_specified']
            newcookie.secure = itm['secure']
            newcookie.expires = itm['expires']
            newcookie.discard = itm['discard']
            newcookie.comment = itm['comment']
            newcookie.comment_url = itm['comment_url']
            newcookie._rest = None
            self.__cookielist.set_cookie(newcookie)
        return True
