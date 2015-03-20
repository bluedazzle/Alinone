from django.core.management.base import BaseCommand
from CronOrder.crontest import *
from CronOrder.models import *
from CronOrder.ele import *
from CronOrder.Aaps import *
from CronOrder.ALO import *
from CronOrder.meituan import *
import os, sys
from apscheduler.schedulers.blocking import BlockingScheduler
from CronOrder.method import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        # # # # catcheleorder(1)
        # # # ordlist = ['12459171300411697']
        # # # ensureleeorder(1,ordlist)
        a = Ele()
        mer = Merchant.objects.get(id=1)
        res = a.catcheorder(mer)
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