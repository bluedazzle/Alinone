from CronOrder.ele import *
from CronOrder.tdd import *
from CronOrder.meituan import *
from AlinLog.models import RunTimeLog

class Alo(object):
    def ensure_order(self, merchantid, order):
        orderid = str(order).split(',')[0]
        platform = str(order).split(',')[1]
        mer = Merchant.objects.filter(id = merchantid)[0]
        if platform == '1':
            tddcat = Tao()
            tddres = tddcat.ensureorder(mer, orderid)
            return tddres
        elif platform == '2':
            elecat = Ele()
            eleres = elecat.ensureorder(mer, orderid)
            return eleres
        elif platform == '3':
            meicat = Mei()
            meires = meicat.ensureOrder(mer, orderid)
            return meires

    def refuse_order(self, merchantid, order):
        orderid = str(order).split(',')[0]
        platform = str(order).split(',')[1]
        print 'refuse_order'
        if len(orderid) < 5:
            return True
        mer = Merchant.objects.filter(id = merchantid)[0]
        if platform == '1':
            tddcat = Tao()
            tddres = tddcat.refuseorder(mer, orderid)
            return tddres
        elif platform == '2':
            elecat = Ele()
            eleres = elecat.refuseorder(mer, orderid)
            return eleres
        elif platform == '3':
            meicat = Mei()
            meires = meicat.refuseOrder(mer, orderid)
            return meires

    def cronOrder(self, merchantid):
        mer = Merchant.objects.filter(id = merchantid)[0]
        try:
            mer.netspider_time = datetime.datetime.now()
            meires = None
            print('%s is online' % mer.name)
            if mer.ele_account != '':
                elecat = Ele()
                eleres = elecat.catcheorder(mer)
            if mer.mei_account != '':
                meicat = Mei()
                meires = meicat.getOrder(mer)
            if mer.tao_account != '':
                tddcat = Tao()
                tddres = tddcat.getpaddingorder(mer)
            mer.save()
            return meires
        except Exception, e:
            mer.save()
            print 'ALO ERROR'
            print e
