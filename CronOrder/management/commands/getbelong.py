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
        senders = Sender.objects.all()
        for itm in senders:
            itm.belongs = get_phone_belong(itm.phone)
            itm.save()
        merchants= Merchant.objects.all()
        for itm in merchants:
            itm.belongs = get_phone_belong(itm.alin_account)
            itm.save()
        print 'success'