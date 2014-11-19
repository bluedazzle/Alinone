from uwsgidecorators import *
from CronOrder.Aaps import *

@spool
def startAPS(args):
    APS = OrderAps()
    print 'aps start'

startAPS.spool()