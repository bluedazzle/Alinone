import qrcode
import os
import datetime
import time

BASE = os.path.dirname(os.path.dirname(__file__))

def createqr(type, qrtext):
    savename = ''
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    if str(type) == '1':
        #http://localhost:8888/search/result?searchtext=18215606355
        qr.add_data('http://100.64.132.52:8888/search/result?searchtext=' + qrtext)
        savename = BASE + '/qrimg/order' + str(str(time.time())[0:10]) + '.png'
    elif str(type) == '2':
        qr.add_data(qrtext + str(time.time())[0:10])
        savename = BASE + '/qrimg/bind' + str(str(time.time())[0:10]) + '.png'
    qr.make(fit=True)
    img = qr.make_image()
    img.save(savename)
    return savename

