from uwsgidecorators import *
from CronOrder.Aaps import *
import uwsgi

@spoolforever
def createback():
    newback = OrderAps()
    return newback

uwsgi.spooler = createback