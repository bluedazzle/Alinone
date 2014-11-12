from django.core.management.base import BaseCommand
from CronOrder.crontest import *
from AlinApi.views import *
from CronOrder.ele import *
from CronOrder.tdd import *
from QRcode.method import *
from CronOrder.models import *
import cookielib
import os,sys
from apscheduler.schedulers.blocking import BlockingScheduler
from CronOrder.method import *
scheduler = BlockingScheduler()
tddcat = None
elecat = None
elecookjar = None
i = 0
# def createnew(merid, autoid):
#     no = DayOrder()
#     no.order_id_alin = str(createAlinOrderNum(1, merid, autoid))
#     createqr(1, createAlinOrderNum(2, merid, autoid))
#     no.address = 'kb363' + str(autoid)
#     no.order_id_old = '0000' + str(autoid)
#     no.order_time = datetime.datetime.now()
#     no.phone = '18215606355'
#     no.origin_price = 13.0
#     no.real_price = 10.0
#     no.order_id_old = '0000000' + str(autoid)
#     no.platform = 1
#     no.status = 1
#     no.promotion = 'nothing'
#     no.merchant = Merchant.objects.filter(id = merid)[0]
#     no.send_time = datetime.datetime.now()
#     no.save()
#     return 'success'

def tick():
    global tddcat
    global elecat
    global i
    global scheduler
    global elecookjar
    mer = Merchant.objects.filter(id = i)[0]
    acttime = mer.update_time.replace(tzinfo = None)
    is_act = isactive(acttime, 60)
    if not is_act:
        mer.is_online = False
        mer.save()
    if mer.is_online is True:
        print('%s is online' % mer.name)
        # res = createnew(2, int(mer.todaynum))
        # res = catcheleorder(i, elecookjar)
        res = elecat.catcheorder()
        # if res is not None:
        #     elecookjar = res
        # else:
        #     elecookjar = None
        # # print res
        # tres = tddcat.getpaddingorder()
        # print tres
    elif mer.is_online is False:
        print('%s is offline,schel will exit' % mer.name)
        scheduler.shutdown()

class Command(BaseCommand):
    def handle(self, *args, **options):
        global i
        global elecat
        global tddcat
        global scheduler
        i = int(args[0])
        tddcat = Tao(merchantid=i)
        elecat = Ele(merchantid=i)
        scheduler.add_job(tick, 'interval', seconds=10)
        print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            pass


