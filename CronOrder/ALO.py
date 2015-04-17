from CronOrder.ele import *
from CronOrder.tdd import *
from CronOrder.meituan import *
from AlinApi.views import isactive
from AlinLog.error import except_handle

class Alo(object):
    def __init__(self, use_proxy=False):
        self.__use_proxy = use_proxy


    def ensure_order(self, merchantid, order):
        orderid = str(order).split(',')[0]
        platform = str(order).split(',')[1]
        if len(orderid) < 5:
            return True
        mer = Merchant.objects.filter(id = merchantid)[0]
        if platform == '1':
            tddcat = Tao()
            tddres = tddcat.ensureorder(mer, orderid)
            return tddres
        elif platform == '2':
            elecat = Ele(merchantid, self.__use_proxy)
            eleres = elecat.ensureorder(mer, orderid)
            return eleres
        elif platform == '3':
            meicat = Mei(merchantid, self.__use_proxy)
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
            elecat = Ele(merchantid, self.__use_proxy)
            eleres = elecat.refuseorder(mer, orderid)
            return eleres
        elif platform == '3':
            meicat = Mei(merchantid, self.__use_proxy)
            meires = meicat.refuseOrder(mer, orderid)
            return meires

    def cronOrder(self, merchantid, first=False):
        mer = Merchant.objects.filter(id = merchantid)[0]
        try:
            if not first:
                nowt = datetime.datetime.now()
                if isactive(mer.netspider_time.replace(tzinfo=None), det=19):
                    return True
            mer.netspider_time = datetime.datetime.now()
            meires = None
            print('%s is online' % mer.name)
            CatcheData.objects.get_or_create(merchant=mer)
            if mer.ele_account != '' and mer.ele_status is True:
                elecat = Ele(merchantid, self.__use_proxy)
                eleres = elecat.catcheorder(mer)
            if mer.mei_account != '' and mer.mei_status is True:
                print 'mei excet'
                meicat = Mei(merchantid, self.__use_proxy)
                meires = meicat.getOrder(mer)
            if mer.tao_account != '' and mer.tao_status is True:
                tddcat = Tao()
                tddres = tddcat.getpaddingorder(mer)
            mer.save()
            return meires
        except Exception, e:
            mer.save()
            print 'ALO ERROR'
            except_handle(e)
