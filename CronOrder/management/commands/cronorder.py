from django.core.management.base import BaseCommand
from CronOrder.crontest import *
from CronOrder.models import *
import os, sys
from apscheduler.schedulers.blocking import BlockingScheduler
<<<<<<< HEAD

scheduler = BlockingScheduler()
i = 0
n = 0
def createnew(name='burgerking'):
    global n
    no = DayOrder()
    no.order_id_alin = '00000000' + str(n)
    no.address = 'kb363' + str(n)
    no.order_id_old = '0000' + str(n)
    no.order_time = datetime.datetime.now()
    no.phone = '1300010' + str(n)
    no.origin_price = 13.0
    no.real_price = 10.0
    no.send_time = datetime.datetime.now()
    no.order_id_old = '0000000' + str(n)
    no.platform = 1
    no.status = 1
    no.promotion = 'nothing'
    no.merchant = Merchant.objects.filter(name = 'burgerking')[0]
    no.save()
    n += 1
=======
from CronOrder.method import *
scheduler = BlockingScheduler()
i = 0
def createnew(merid, autoid):
    no = DayOrder()
    no.order_id_alin = str(createAlinOrderNum(1, merid, autoid))
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
    no.merchant = Merchant.objects.filter(id = merid)[0]
    no.send_time = datetime.datetime.now()
    no.save()
>>>>>>> 30fc746ccc89d7064d9da3134a3e1ee06d056c10
    return 'success'

def tick():
    global i
    global scheduler
    mer = Merchant.objects.filter(id = i)[0]
    if mer.is_online is True:
<<<<<<< HEAD
        mer.tao_account = 'success'
        mer.save()
        print('%s is online' % mer.name)
        res = createnew(str(mer.name))
=======
        print('%s is online' % mer.name)
        res = createnew(2, int(mer.todaynum))
        mer.todaynum += 1
        mer.save()
>>>>>>> 30fc746ccc89d7064d9da3134a3e1ee06d056c10
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


