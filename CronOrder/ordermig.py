from CronOrder.models import *

def migrateorder():
    dayorder_list = DayOrder.objects.all()
    for itm in dayorder_list:
        newto = TotalOrder()
        newto.order_time = itm.order_time
        newto.address = itm.address
        newto.finish_by = itm.finish_by
        newto.merchant = itm.merchant
        newto.bind_sender = itm.bind_sender
        newto.note = itm.note
        newto.order_id_alin = itm.order_id_alin
        newto.order_id_old = itm.order_id_old
        newto.origin_price = itm.origin_price
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
        return True
    else:
        return False