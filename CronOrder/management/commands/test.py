from django.core.management.base import BaseCommand
from CronOrder.crontest import *
from CronOrder.models import *
from CronOrder.ele import *
from CronOrder.Aaps import *
import os, sys
from apscheduler.schedulers.blocking import BlockingScheduler
from CronOrder.method import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        # # # catcheleorder(1)
        # # ordlist = ['12459171300411697']
        # # ensureleeorder(1,ordlist)
        # a = Ele(1)
        # res = a.catcheorder()
        # print res
        a = OrderAps()
        res = a.addJobs('1')
        # print res