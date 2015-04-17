from django.core.management.base import BaseCommand
from CronOrder.crontest import *
from CronOrder.models import *
import os, sys
# from apscheduler.schedulers.blocking import BlockingScheduler
from CronOrder.method import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        # merlist = Merchant.objects.all()
        # for itm in merlist:
        #     itm.todaynum = 1
        #     itm.save()
        # print 'succ'