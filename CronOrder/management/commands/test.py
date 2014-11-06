from django.core.management.base import BaseCommand
from CronOrder.crontest import *
from CronOrder.models import *
from CronOrder.ele import *
import os, sys
from apscheduler.schedulers.blocking import BlockingScheduler
from CronOrder.method import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        catcheleorder(2)