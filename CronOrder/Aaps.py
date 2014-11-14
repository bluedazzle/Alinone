from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import ConflictingIdError
from AlinApi.views import *
from CronOrder.ele import *
from CronOrder.tdd import *
from CronOrder.models import *
from apscheduler.jobstores.base import JobLookupError
from apscheduler.events import *
from apscheduler.events import JobExecutionEvent
import datetime

class OrderAps(object):
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler._daemon = False
        self.tdict = {}
        self.edict = {}
        self.initJobs()
        self.scheduler.start()

    def ifruning(self, merchantid):
        merchantid = str(merchantid)
        job = self.scheduler.get_job(job_id=merchantid)
        if job is None:
            return False
        else:
            return True

    def initJobs(self):
        return True

    def stopAps(self):
        self.scheduler.shutdown(wait=True)
        return True

    def addJobs(self, merchantid):
        if self.ifruning(merchantid):
            return True
        try:
            self.scheduler.add_job(self.cronOrder, 'interval', (str(merchantid),), seconds = 10, id=str(merchantid), name=str(merchantid))
            cumer = Merchant.objects.filter(id = merchantid)[0]
            if cumer.ele_account != '':
                newele = Ele(merchantid=str(merchantid))
                self.edict[merchantid] = newele
            if cumer.tao_account != '':
                newtdd = Tao(merchantid=str(merchantid))
                self.tdict[merchantid] = newtdd
            return True
        except Exception, e:
            print e
            return False

    def removeJobs(self, merchantid):
        try:
            self.scheduler.remove_job(job_id=str(merchantid))
            self.tdict[str(merchantid)] = None
            self.edict[str(merchantid)] = None
            return True
        except Exception, e:
            print e
            return False

    def cronOrder(self, merchantid):
        try:
            mer = Merchant.objects.filter(id = merchantid)[0]
            acttime = mer.update_time.replace(tzinfo = None)
            is_act = isactive(acttime, 60)
            mer.netspider_time = datetime.datetime.now()
            if not is_act:
                mer.is_online = False
            mer.save()
            if is_act:
                print('%s is online' % mer.name)
                if str(merchantid) in self.tdict and self.tdict[str(merchantid)] is not None:
                    tddcat = self.tdict[str(merchantid)]
                    tres = tddcat.getpaddingorder()
                    if tres is None:
                        mer.tdd_status = False
                    else:
                        mer.tdd_status = True
                if str(merchantid) in self.edict and self.edict[str(merchantid)] is not None:
                    elecat = self.edict[str(merchantid)]
                    res = elecat.catcheorder()
            # tres = tddcat.getpaddingorder()
            # print tres
                    if res is None:
                        mer.ele_status = False
                        mer.save()
                    elif res is False:
                        mer.ele_status = True
                        mer.save()
                    else:
                        print 'res is : ' + str(res)
                        mer.todaynum = int(res)
                        mer.ele_status = True
                        mer.save()
            else:
                print('%s is offline,schel will exit' % mer.name)
                ress = self.removeJobs(merchantid)
                print ress
        except Exception, e:
            print e


