from django.core.management.base import BaseCommand
from CronOrder.crontest import *
from CronOrder.models import *
from CronOrder.ele import *
from CronOrder.Aaps import *
from CronOrder.ALO import *
from CronOrder.meituan import *
import os, sys
from django.db.models.query import QuerySet
# from apscheduler.schedulers.blocking import BlockingScheduler
from CronOrder.method import *
from django.db import models
from AlinApi.method import model_serializer
import simplejson
import json

class Command(BaseCommand):
    def handle(self, *args, **options):
        # # # # catcheleorder(1)
        # # # ordlist = ['12459171300411697']
        # # # ensureleeorder(1,ordlist)
        # a = Ele()
        # mer = Merchant.objects.get(id=1)
        # res = a.catcheorder(mer)
        mer = Merchant.objects.get(id=1)
        # a = Mei()
        # res = a.getOrder(mer)
        # # print res
        # a = OrderAps()
        # res = a.addJobs('1')
        # # print res
        # al = Alo()
        # # al.cronOrder(str(1))
        # meit = mei(1)
        # meit.get_token()
        # print meit.token
        # res = meit.getOrder()
        # if res is True:
        #     print 'success'
        a = DayOrder.objects.all()
        # print as[1].serializer()
        # print type(a)
        # # print a.latest('alin_account')
        # # print a.earliest('alin_account')
        # # print a.__reduce__()
        e = a[0]
        d = a[1]
        # # print isinstance(a, QuerySet)
        # print type(e)
        # f = [e, d]
        # print isinstance(e, models.Model)
        # print type(f)
        ff = []
        # # print e.__dict__
        # for i in a:
        #     ff.append(i.serializer())
        # b = json.dumps(ff)
        z = model_serializer(a, datetime_format='timestamp', serializer='dict')
        print z
        # print b
        # print d.test()
        # print e.test()
        # for i in e.test():
            # print getattr(e, i.name)
        # print e.test()