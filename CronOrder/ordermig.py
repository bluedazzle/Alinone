#coding: utf-8
from CronOrder.models import *
from AlinLog.models import *

def migrateorder(args = None):
    dayorder_list = DayOrder.objects.all()
    totalnum = dayorder_list.count()
    for itm in dayorder_list:
        newto = TotalOrder()
        newto.order_time = itm.order_time
        newto.address = itm.address
        print itm.finish_by
        newto.finish_by = itm.finish_by
        newto.merchant = itm.merchant
        newto.bind_sender = itm.bind_sender
        newto.note = itm.note
        newto.order_id_alin = itm.order_id_alin
        newto.order_id_old = itm.order_id_old
        newto.origin_price = itm.origin_price
        if str(itm.status) != '4' or str(itm.status) != '5':
            newto.status = 4
            newto.finish_by = itm.bind_sender
        else:
            newto.status = itm.status
        newto.pay = itm.pay
        newto.phone = itm.phone
        newto.send_time = itm.send_time
        newto.platform = itm.platform
        newto.promotion = itm.promotion
        newto.qr_path = itm.qr_path
        newto.real_price = itm.real_price
        newto.save()
    tdish_list = Dish.objects.all()
    for item in tdish_list:
        newtd = Tdish()
        newtd.dish_count = item.dish_count
        newtd.dish_name = item.dish_name
        newtd.dish_price = item.dish_price
        newtd.order = TotalOrder.objects.get(order_id_alin = str(item.order.order_id_alin))
        newtd.save()
    dayorder_list = DayOrder.objects.all().delete()
    if dayorder_list is None:
        content = '迁移订单成功，迁移数目：' + str(totalnum) + '条'
        print content
        newlog = CronLog()
        newlog.status = True
        newlog.content = content
        newlog.ltype = 3
        newlog.save()
        return True
    else:
        return False

def resetToken(args = None):
    cache_list = CatcheData.objects.all()
    totalnum = cache_list.count()
    content = '刷新elecookie成功，刷新数目：' + str(totalnum) + '条'
    for itm in cache_list:
        itm.ele_cookie = ''
        itm.save()
    newlog = CronLog()
    newlog.status = True
    newlog.content = content
    newlog.ltype = 4
    newlog.save()