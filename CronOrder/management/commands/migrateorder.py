from django.core.management.base import BaseCommand
from CronOrder.ordermig import *
class Command(BaseCommand):
    def handle(self, *args, **options):
        res = migrateorder()
        print res