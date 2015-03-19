import requests

class NetProcess(object):
    def __init__(self):
        self.__proxy = ''
        self.__cookies = {}
        self.__usecookies = False
        self.__headers = {}
        self.__useheaders = False

    def getCookies(self): return self.__cookies
    def setCookies(self, value):self.__cookies = value
    Cookies = property(getCookies, setCookies, "Property CookieList")

    def getProxy(self): return self.__proxy
    def setProxy(self, value):self.__proxy = value
    Proxy = property(getProxy, setProxy, "Property Proxy")

    def getHeaders(self): return self.__headers
    def setHeaders(self, value):self.__headers = value
    Headers = property(getHeaders, setHeaders, "Property Headers")



    def GetResFromRequest(self, method, requrl, encodemethod='utf-8', postDic={}, reqdata='', use_proxy=False):
        res = None
        try:
            if str(method).upper() == 'POST':
                if use_proxy:
                    proxy = {"http": self.__proxy, }
                    res = requests.post(requrl, data=postDic, proxies=proxy, headers=self.__headers)
                else:
                    res = requests.post(requrl, data=postDic, cookies=self.__cookies, headers=self.__headers)
            elif str(method).upper() == 'GET':
                if use_proxy:
                    proxy = {"http": self.__proxy, }
                    res = requests.get(requrl, proxies=proxy, cookies=self.__cookies, headers=self.__headers)
                else:
                    res = requests.get(requrl, cookies=self.__cookies, headers=self.__headers)
            self.__cookies = res.cookies
            print res.headers
            return res.content
        except Exception, e:
            print e.message
            print e
            return e
        finally:
            pass

    def OutPutCookie(self):
        res = {}
        for (itm, key) in self.__cookies.items():
            res[itm] = key
        return res

    def SetCookie(self, cookiestr):
        cookielist = eval(cookiestr)
        self.__cookies = cookielist
        self.__usecookies = True
        return True

    def SetHeaders(self, headerdic):
        self.__headers = headerdic
        self.__useheaders = True
        return True

# net = NetProcess()
# postdic = {'username': 'guaishushuliansuo', 'password': '18215605920'}
# r = net.GetResFromRequest('POST','http://napos.ele.me/auth/doLogin', postDic=postdic)
# c = str(net.OutPutCookie())
# print r
# net.SetCookie(c)
# d = net.GetResFromRequest('GET', 'http://napos.ele.me/order/list?list=unprocessed_waimai&t=1407000000')
# print d

# net = NetProcess()
# postdic = {'id': 8}
# net.Proxy = '124.88.67.24:80'
# # r = net.GetResFromRequest('GET', 'http://vote.stuhome.net/', use_proxy=True)
# # cok = str(net.OutPutCookie())
# # print cok
# # net.SetCookie(cok)
# headerdic = {'X-Requested-With': 'XMLHttpRequest',
#              'User-Agent': 'Dalvik/1.6.0 (Linux; U; Android 4.1.1; MI 2S MIUI/4.11.7)'}
# net.SetHeaders(headerdic)
# r = net.GetResFromRequest('POST', 'http://vote.stuhome.net/Index/Index/loveArticle', use_proxy=True)
# print r