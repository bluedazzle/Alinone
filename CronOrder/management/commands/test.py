from django.core.management.base import BaseCommand
from CronOrder.crontest import *
from CronOrder.models import *
import os, sys
from apscheduler.schedulers.blocking import BlockingScheduler
from CronOrder.method import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        autoid = args[0]
        no = DayOrder()
        no.order_id_alin = str(createAlinOrderNum(1, 1, autoid))
        no.address = 'kb363' + str(autoid)
        no.order_id_old = '0000' + str(autoid)
        no.order_time = datetime.datetime.now()
        no.phone = '1300010' + str(autoid)
        no.origin_price = 13.0
        no.real_price = 10.0
        no.order_id_old = '0000000' + str(autoid)
        no.platform = 1
        no.status = 1
        no.promotion = 'nothing'
        no.merchant = Merchant.objects.filter(id = 1)[0]
        no.send_time = datetime.datetime.now()
        no.save()
        print 'succ'