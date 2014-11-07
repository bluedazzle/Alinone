from CronOrder.models import *
import datetime
class OrderTest():
    def __init__(self):
        self.__index = 10

    def createnew(self, name='burgerking'):
        no = DayOrder()
        no.order_id_alin = '0000' + str(self.__index)
        no.address = 'kb363' + str(self.__index)
        no.order_id_old = '0000' + str(self.__index)
        no.order_time = datetime.now()
        no.phone = '1300010' + str(self.__index)
        no.origin_price = 13.0
        no.real_price = 10.0
        no.send_time = datetime.now()
        no.order_id_old = '0000' + str(self.__index)
        no.platform = 1
        no.promotion = 'nothing'
        no.merchant = Merchant.objects.filter(name = name)[0]
        no.save()
        print 'ordersavesuccess'

        dish = Dish()
        dish.dish_name = 'testdish'
        dish.dish_count = 3
        dish.dish_price = 13.0
        dish.order = no
        dish.save()

        self.__index += 1

        return 'success'
