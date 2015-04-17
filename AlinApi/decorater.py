from AlinApi.models import ApiTimes
from django.http import HttpResponse
from AlinApi.method import *

def api_times(func):
    def exect(*args, **kw):
        body = {}
        req = args[0]
        ip = req.META['REMOTE_ADDR']
        uri = req.META['PATH_INFO']
        api_t = ApiTimes.objects.get_or_create(ip=ip)[0]
        api_t.req_times += 1
        # if api_t.req_times > 5:
        #     body['msg'] = 'api times upbound'
        #     return HttpResponse(encodejson(30, body), content_type='application/json')
        api_t.save()
        print 'address:%s request %s, total %i' % (ip, uri, api_t.req_times)
        res = func(*args, **kw)
        if isinstance(res, HttpResponse):
            print 'req call success'
        else:
            print 'req call fail'
        return res
    return exect