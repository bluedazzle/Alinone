# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from CronOrder.crontest import *
from CronOrder.models import *
import os, sys
# from apscheduler.schedulers.blocking import BlockingScheduler
from QRcode.method import createqr
from CronOrder.method import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        username = args[0]
        print username
        merchant = Merchant.objects.get(alin_account=username)
        thiscount = int(DayOrder.objects.filter(merchant=merchant, platform=11).count()) + 1
        totalcount = int(DayOrder.objects.filter(merchant=merchant).count()) + 1
        for i in range(6):
            newid = createAlinOrderNum(11, merchant.id, thiscount)
            qrres = createqr(1, newid)
            neworder = DayOrder(order_id_alin=newid,
                                order_id_old='1111',
                                phone=18215606355,
                                pay=True,
                                address='KB258',
                                platform=11,
                                plat_num=5,
                                note='',
                                origin_price=18,
                                real_price=18,
                                status=1,
                                merchant=merchant,
                                order_time=datetime.datetime.now(),
                                send_time=datetime.datetime.now(),
                                day_num=totalcount,
                                qr_path=qrres)
            neworder.save()
            newdish = Dish(dish_name='宫保鸡丁', dish_price=12, dish_count=1, order=neworder)
            newdish.save()
            newdish1 = Dish(dish_name='珍珠大吊饭', dish_price=1, dish_count=2, order=neworder)
            newdish1.save()
            newdish2 = Dish(dish_name='可口可乐', dish_price=2, dish_count=2, order=neworder)
            newdish2.save()
            thiscount += 1
            totalcount += 1