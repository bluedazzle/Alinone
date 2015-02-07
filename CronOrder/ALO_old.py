from CronOrder.ele import *
from CronOrder.tdd import *
from CronOrder.meituan import *
from AlinLog.models import RunTimeLog

class Alo(object):
    def __init__(self):
        self.edict = {}
        self.tdict = {}
        self.mdict = {}

    def ensure_order(self, merchantid, order):
        orderid = str(order).split(',')[0]
        platform = str(order).split(',')[1]
        mer = Merchant.objects.filter(id = merchantid)[0]
        if platform == '1':
            if str(merchantid) in self.tdict and self.tdict[str(merchantid)] is not None:
                tddcat = self.tdict[str(merchantid)]
                tres = tddcat.ensureorder(orderid)
                if tres is None:
                    mer.tdd_status = False
                    self.tdict[str(mer.id)] = None
                    return False
                else:
                    mer.tdd_status = True
            elif mer.tao_account != '':
                newtdd = Tao(session = str(mer.tao_sessionkey), merchantid = str(mer.id))
                tres = newtdd.ensureorder(orderid)
                if tres is None:
                    mer.tdd_status = False
                    return False
                else:
                    mer.tdd_status = True
                    self.tdict[str(mer.id)] = newtdd
        elif platform == '2':
            if str(merchantid) in self.edict and self.edict[str(merchantid)] is not None:
                elecat = self.edict[str(merchantid)]
                res = elecat.ensureorder(orderid)
                if res is None:
                    mer.ele_status = False
                    self.edict[str(merchantid)] = None
                    return False
                elif res is False:
                    mer.ele_status = True
                    return False
                else:
                    mer.ele_status = True
            elif mer.ele_account != '':
                newele = Ele(merchantid=str(mer.id))
                eres = newele.ensureorder(orderid)
                if eres is None:
                    mer.ele_status = False
                    return False
                elif eres is False:
                    mer.ele_status = True
                    self.edict[str(mer.id)] = newele
                    return False
                else:
                    mer.ele_status = True
                    self.edict[str(mer.id)] = newele
        elif platform == '3':
            if str(merchantid) in self.mdict and self.mdict[str(merchantid)] is not None:
                meicat = self.mdict[str(merchantid)]
                res = meicat.ensureOrder(orderid)
                if res is None:
                    mer.mei_status = False
                    self.mdict[str(merchantid)] = None
                    return False
                elif res is False:
                    mer.mei_status = True
                    return False
                elif res == 'c cancel':
                    mer.mei_status = True
                    return 'c cancel'
                else:
                    mer.mei_status = True
            elif mer.mei_account != '':
                newmei = mei(merchantid=str(mer.id))
                mres = newmei.ensureOrder(orderid)
                if mres is None:
                    mer.mei_status = False
                    return False
                elif mres is False:
                    mer.mei_status = True
                    self.mdict[str(mer.id)] = newmei
                    return False
                else:
                    mer.mei_status = True
                    self.mdict[str(mer.id)] = newmei
        mer.save()
        return True

    def refuse_order(self, merchantid, order):
        orderid = str(order).split(',')[0]
        platform = str(order).split(',')[1]
        mer = Merchant.objects.filter(id = merchantid)[0]
        if platform == '1':
            if str(merchantid) in self.tdict and self.tdict[str(merchantid)] is not None:
                tddcat = self.tdict[str(merchantid)]
                tres = tddcat.refuseorder(orderid)
                if tres is None:
                    mer.tdd_status = False
                    self.tdict[str(mer.id)] = None
                    return False
                else:
                    mer.tdd_status = True
            elif mer.tao_account != '':
                newtdd = Tao(session = str(mer.tao_sessionkey), merchantid = str(mer.id))
                tres = newtdd.refuseorder(orderid)
                if tres is None:
                    mer.tdd_status = False
                    return False
                else:
                    mer.tdd_status = True
                    self.tdict[str(mer.id)] = newtdd
        elif platform == '2':
            if str(merchantid) in self.edict and self.edict[str(merchantid)] is not None:
                elecat = self.edict[str(merchantid)]
                res = elecat.refuseorder(orderid)
                if res is None:
                    mer.ele_status = False
                    self.edict[str(merchantid)] = None
                    return False
                elif res is False:
                    mer.ele_status = True
                else:
                    mer.ele_status = True
            elif mer.ele_account != '':
                newele = Ele(merchantid=str(mer.id))
                eres = newele.refuseorder(orderid)
                if eres is None:
                    mer.ele_status = False
                    return False
                elif eres is False:
                    mer.ele_status = True
                    self.edict[str(mer.id)] = newele
                else:
                    mer.ele_status = True
                    self.edict[str(mer.id)] = newele
        elif platform == '3':
            if str(merchantid) in self.mdict and self.mdict[str(merchantid)] is not None:
                meicat = self.mdict[str(merchantid)]
                res = meicat.refuseOrder(orderid)
                if res is None:
                    mer.mei_status = False
                    self.mdict[str(merchantid)] = None
                    return False
                elif res is False:
                    mer.mei_status = True
                else:
                    mer.mei_status = True
            elif mer.mei_account != '':
                newmei = mei(merchantid=str(mer.id))
                mres = newmei.refuseOrder(orderid)
                if mres is None:
                    mer.mei_status = False
                    return False
                elif mres is False:
                    mer.mei_status = True
                    self.mdict[str(mer.id)] = newmei
                else:
                    mer.mei_status = True
                    self.mdict[str(mer.id)] = newmei
        mer.save()
        return True

    def cronOrder(self, merchantid):
        mer = Merchant.objects.filter(id = merchantid)[0]
        try:
            mer.netspider_time = datetime.datetime.now()
            print('%s is online' % mer.name)
            # if str(merchantid) in self.tdict and self.tdict[str(merchantid)] is not None:
            #     tddcat = self.tdict[str(merchantid)]
            #     tres = tddcat.getpaddingorder()
            #     if tres is None:
            #         mer.tdd_status = False
            #         self.tdict[str(mer.id)] = None
            #     else:
            #         mer.tdd_status = True
            # elif mer.tao_account != '':
            #     newtdd = Tao(session = str(mer.tao_sessionkey), merchantid = str(mer.id))
            #     tres = newtdd.getpaddingorder()
            #     if tres is None:
            #         mer.tdd_status = False
            #     else:
            #         mer.tdd_status = True
            #         self.tdict[str(mer.id)] = newtdd
            if str(merchantid) in self.edict and self.edict[str(merchantid)] is not None:
                elecat = self.edict[str(merchantid)]
                res = elecat.catcheorder()
                if res is None:
                    mer.ele_status = False
                    self.edict[str(merchantid)] = None
                elif res is False:
                    mer.ele_status = True
                else:
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
                    mer.ele_status = True
                    self.edict[str(mer.id)] = newele
            if str(merchantid) in self.mdict and self.mdict[str(merchantid)] is not None:
                print "mei haved"
                meicat = self.mdict[str(merchantid)]
                res = meicat.getOrder()
                if res is None:
                    mer.mei_status = False
                    self.mdict[str(merchantid)] = None
                elif res is False:
                    mer.mei_status = True
                else:
                    mer.mei_status = True
            elif mer.mei_account != '':
                print 'mei new'
                newmei = mei(merchantid=str(mer.id))
                mres = newmei.getOrder()
                print 'mres'
                print mres
                if mres is None:
                    mer.mei_status = False
                elif mres is False:
                    mer.mei_status = True
                    self.mdict[str(mer.id)] = newmei
                else:
                    mer.mei_status = True
                    self.mdict[str(mer.id)] = newmei
            mer.save()
        except Exception, e:
            mer.save()
            print e