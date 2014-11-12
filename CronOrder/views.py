from django.shortcuts import render
from CronOrder.models import *
from django.http import HttpResponse
# Create your views here.
import datetime
i = 0
def addtest(req):
    global i
    no = DayOrder()
    no.order_id_alin = '00000000' + str(i)
    no.address = 'kb363' + str(i)
    no.order_id_old = '0000' + str(i)
    no.order_time = datetime.datetime.now()
    no.phone = '1300010' + str(i)
    no.origin_price = 13.0
    no.real_price = 10.0
    no.send_time = datetime.datetime.now()
    no.order_id_old = '0000000' + str(i)
    no.platform = 1
    no.status = 1
    no.promotion = 'nothing'
    no.merchant = Merchant.objects.filter(name = 'burgerking')[0]
    no.save()
    i += 1

    return HttpResponse('success')