from django.core.management.base import BaseCommand
from CronOrder.crontest import *
from CronOrder.ele import *
from QRcode.method import *
from CronOrder.models import *
import os, sys
from apscheduler.schedulers.blocking import BlockingScheduler
from CronOrder.method import *
scheduler = BlockingScheduler()
i = 0
def createnew(merid, autoid):
    no = DayOrder()
    no.order_id_alin = str(createAlinOrderNum(1, merid, autoid))
    createqr(1, createAlinOrderNum(2, merid, autoid))
    no.address = 'kb363' + str(autoid)
    no.order_id_old = '0000' + str(autoid)
    no.order_time = datetime.datetime.now()
    no.phone = '18215606355'
    no.origin_price = 13.0
    no.real_price = 10.0
    no.order_id_old = '0000000' + str(autoid)
    no.platform = 1
    no.status = 1
    no.promotion = 'nothing'
    no.merchant = Merchant.objects.filter(id = merid)[0]
    no.send_time = datetime.datetime.now()
    no.save()
    return 'success'

def tick():
    global i
    global scheduler
    mer = Merchant.objects.filter(id = i)[0]
    if mer.is_online is True:
        print('%s is online' % mer.name)
        # res = createnew(2, int(mer.todaynum))
        res = catcheleorder(2, int(mer.todaynum))
        mer.todaynum += 1
        mer.save()
        print res
    elif mer.is_online is False:
        print('%s is offline,schel will exit' % mer.name)
        scheduler.shutdown()

class Command(BaseCommand):
    def handle(self, *args, **options):
        global i
        global scheduler
        i = int(args[0])
        scheduler.add_job(tick, 'interval', seconds=5)
        print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            pass


