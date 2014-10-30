import qrcode
import os
import datetime
import time
from CronOrder.models import *

BASE = os.path.dirname(os.path.dirname(__file__))

def createqr(type, qrtext):
    savename = ''
    filename = ''
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    if str(type) == '1':
        if len(qrtext) != 22:
            return None
        #http://localhost:8888/search/result?searchtext=18215606355
        qr.add_data('http://www.chafanbao.com/search/result?searchtext=' + qrtext)
        filename = 'order' + str(str(time.time())[0:10]) + '.png'
        savename = BASE + '/qrimg/' + filename
        res = DayOrder.objects.filter(order_id_alin = qrtext)
        if res.count() > 0:
            res[0].qr_path = filename
            res[0].save()
    elif str(type) == '2':
        qrtext = '%08i' % int(qrtext)
        qr.add_data(qrtext + str(time.time())[0:10])
        filename = 'bind' + str(str(time.time())[0:10]) + '.png'
        savename = BASE + '/qrimg/' + filename
        res = Merchant.objects.filter(id = int(qrtext))
        if res.count() > 0:
            res[0].bind_pic = filename
            res[0].save()
    qr.make(fit=True)
    img = qr.make_image()
    img.save(savename)
    return filename
