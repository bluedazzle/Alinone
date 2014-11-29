# -*- coding: utf-8 -*-
import top.api
import copy
from QRcode.method import *
from CronOrder.method import *
from CronOrder.models import *
# acc:18215605920
# pass w976624
# session: 6102a219a83b80ed25580ca6885ac1b97ae8435b2b178f7763031727
# refresh_token: 6101d21350ab8f837e7d3c24ad98d1cfce0641f6091874e763031727
# sessionkey = '6102a219a83b80ed25580ca6885ac1b97ae8435b2b178f7763031727'
# top.setDefaultAppInfo("23030341", "914d2762a7e1d721c0b999a08c3869e7")
#
# req = top.api.TradeWaimaiGetRequest()
#
# req.store_id = 238307
# req.is_all = true
# req.max_size = 20
# try:
#     resp = req.getResponse(sessionkey)
#     print resp
#     print resp['store_id']
# except Exception, e:
#     print e

class Tao(object):
    def __init__(self, session = '6102a219a83b80ed25580ca6885ac1b97ae8435b2b178f7763031727', merchantid = 1):
        self.appkey = '23030341'
        self.sessionkey = session
        self.merchantid = merchantid
        self.shopid = ''
        self.secret = '914d2762a7e1d721c0b999a08c3869e7'


    def getshopid(self):
        top.setDefaultAppInfo(self.appkey, self.secret)
        req = top.api.WaimaiShopListRequest()
        req.page = 1
        req.page_size = 20
        try:
            resp = req.getResponse(self.sessionkey)
            res = resp['waimai_shop_list_response']
            resp = res['result']
            res = resp['takeout_summary_infos']
            resp = res['takeout_shop_summary_info'][0]
            shopid = resp['shopid']
            # curmer_list = Merchant.objects.filter(id = self.merchantid)
            # if curmer_list.count() > 0:
            #     curmer = curmer_list[0]
            #     curmer.tao_shopid = shopid
            #     curmer.save()
            self.shopid = shopid
            print shopid
        except Exception, e:
            self.errorhandle(e)
    #         errorcode=27 message
    def gettest(self):
        with open('nap.txt', 'r') as f1:
            res = ''
            line = f1.readline()
            while line:
                res += line
                line = f1.readline()
        return res

    def ensureorder(self, orderid):
        top.setDefaultAppInfo(self.appkey, self.secret)
        req = top.api.TradeWaimaiConfirmRequest()
        req.order_id = orderid
        try:
            resp = req.getResponse(self.sessionkey)
            if resp['ret_code'] == '1':
                return True
            else:
                return False
        except Exception, e:
            self.errorhandle(e)

    def refuseorder(self, orderid):
        top.setDefaultAppInfo(self.appkey, self.secret)
        req = top.api.TradeWaimaiRefuseRequest()
        req.order_id = orderid
        req.reason = 'too busy'
        try:
            resp = req.getResponse(self.sessionkey)
            if resp['ret_code'] == '1':
                return True
            else:
                return False
        except Exception, e:
            self.errorhandle(e)

    def getpaddingorder(self):
        orderid_list = []
        top.setDefaultAppInfo(self.appkey, self.secret)
        if self.shopid == '':
            self.getshopid()
        req = top.api.WaimaiOrderIndexGetRequest()
        req.store_id = self.shopid
        req.page_size = 20

        # try:
        resp = req.getResponse(self.sessionkey)
        # resp = eval(self.gettest())
        res = resp['waimai_order_index_get_response']
        if str(res) != '{}':
            curusr_list = Merchant.objects.filter(id = self.merchantid)
            if curusr_list.count() == 0:
                return None
            curusr = curusr_list[0]
            auto_id = int(DayOrder.objects.filter(merchant = curusr, platform = int(1)).count()) + 1
            resp = res['result']
            res = resp['result_list']
            resp = res['takeout_third_order']
            for itm in resp:
                orderid_list.append(copy.copy(itm['id']))
                req = top.api.WaimaiOrderSingleGetRequest()
                req.order_id = str(itm['id'])
                resp = req.getResponse(self.sessionkey)
                res = resp['waimai_order_single_get_response']
                if str(res) != '{}':
                    resp = res['result']
                    orderid = resp['order_id']
                    ifhave = DayOrder.objects.filter(order_id_old = str(orderid))
                    if ifhave.count() > 0:
                # print 'break'
                # print auto_id + 1
                        continue
                    newid = createAlinOrderNum(1, self.merchantid, auto_id)
                    qrres = createqr(1, newid)
                    auto_id += 1
                    neworder = DayOrder()
                    neworder.address = str(resp['address'])
                    neworder.order_id_old = str(resp['order_id'])
                    neworder.order_id_alin = newid
                    neworder.qr_path = qrres
                    neworder.pay = True
                    neworder.platform = 1
                    neworder.promotion = 'nothing'
                    neworder.real_price = float(str(resp['total_pay']))
                    neworder.order_time = str(resp['create_time'])
                    neworder.send_time = str(resp['start_deliverytime'])
                    neworder.note = str(resp['note'])
                    neworder.merchant = Merchant.objects.get(id = self.merchantid)
                    neworder.save()
                    curusr.save()
                    # print resp['address']
                    # print resp['id']
                    # print resp['total_pay']
                    # print resp['start_deliverytime']
                    # print resp['create_time']
                    # print resp['note']
                    sonres = resp['user_address']
                    print sonres['mobile']
                    dishlist = resp['goods_list']
                    dishs = dishlist['order_goods']
                    for itm in dishs:
                        newdish = Dish()
                        newdish.dish_count = str(itm['count'])
                        newdish.dish_name = str(itm['name'])
                        newdish.dish_price = str(itm['real_price'])
                        newdish.order = DayOrder.objects.get(order_id_alin = newid)
                        newdish.save()
                        # print itm['name']
                        # print itm['count']
                        # print itm['real_price']
            return True
        else:
            return False
        # except Exception, e:
        #     print e
            # self.errorhandle(e)

    def errorhandle(self, e):
        errcode = e.errorcode
        errmes = ''
        errstatus = False
        if errcode == 27:
            errmes = 'Session错误'
        else:
            errmes = e.message
        print errmes
        curmer_list = Merchant.objects.filter(id = self.merchantid)
        if curmer_list.count() > 0:
            curmer = curmer_list[0]
            curmer.tao_message = errmes
            curmer.tao_status = errstatus
            curmer.save()
        return None