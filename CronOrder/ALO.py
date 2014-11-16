from CronOrder.models import *
from CronOrder.ele import *
from CronOrder.tdd import *

class Alo(object):
    def __init__(self):
        self.edict = {}
        self.tdict = {}
        self.mdict = {}

    def cronOrder(self, merchantid):
        mer = Merchant.objects.filter(id = merchantid)[0]
        try:
            mer.netspider_time = datetime.datetime.now()
            print('%s is online' % mer.name)
            if str(merchantid) in self.tdict and self.tdict[str(merchantid)] is not None:
                tddcat = self.tdict[str(merchantid)]
                tres = tddcat.getpaddingorder()
                if tres is None:
                    mer.tdd_status = False
                    self.tdict[str(mer.id)] = None
                else:
                    mer.tdd_status = True
            elif mer.tao_account != '':
                newtdd = Tao(merchantid = str(mer.id))
                tres = newtdd.getpaddingorder()
                if tres is None:
                    mer.tdd_status = False
                else:
                    mer.tdd_status = True
                    self.tdict[str(mer.id)] = newtdd
            if str(merchantid) in self.edict and self.edict[str(merchantid)] is not None:
                elecat = self.edict[str(merchantid)]
                res = elecat.catcheorder()
                if res is None:
                    mer.ele_status = False
                    self.edict[str(merchantid)] = None
                elif res is False:
                    mer.ele_status = True
                else:
                    mer.todaynum = int(res)
                    mer.ele_status = True
            elif mer.ele_account != '':
                newele = Ele(merchantid=str(mer.id))
                eres = newele.catcheorder()
                if eres is None:
                    mer.ele_status = False
                elif eres is False:
                    mer.ele_status = True
                    self.edict[str(mer.id)] = newele
                else:
                    mer.todaynum = int(eres)
                    mer.ele_status = True
                    self.edict[str(mer.id)] = newele
            mer.save()
        except Exception, e:
            mer.save()
            print e