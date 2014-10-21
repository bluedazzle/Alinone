import datetime
from django.http import Http404

def createAlinOrderNum(platid,merchantid,autoid):
    #try:
        odate = datetime.date.today()
        odate = str(odate).replace('-', '')
        auto_format = ''
        plat_format = ''
        merchant_format = ''
        if len(str(platid)) <= 2 and len(str(merchantid)) <= 8:
            auto_format = '%04i' % int(autoid)
            plat_format = '%02i' % int(platid)
            merchant_format = '%08i' % int(merchantid)
        else:
            return 0
        aon = str(odate) + plat_format + merchant_format + auto_format
        return aon
    # except Exception, e:
	# 	raise Http404
	# else:
	# 	pass
	# finally:
	# 	pass
