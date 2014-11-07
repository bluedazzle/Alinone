from django.core.management.base import BaseCommand
from ProxyWork.method import *
import os, sys
from apscheduler.schedulers.blocking import BlockingScheduler
from CronOrder.method import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        checkproxy()