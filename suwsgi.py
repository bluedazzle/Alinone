import os
import uwsgi
from CronOrder.ele import *
from CronOrder.ordermig import *
from CronOrder.method import *
from ProxyWork.method import *
import sys
reload(sys)
sys.setdefaultencoding('utf8')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SeaSite.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

uwsgi.register_signal(80, "", resetToken)
uwsgi.add_timer(80, 1800)
uwsgi.register_signal(82, "", getproxy)
uwsgi.add_cron(82, 0, 10, -1, -1, -1)
uwsgi.register_signal(84, "", getproxy)
uwsgi.add_cron(84, 0, 15, -1, -1, -1)
uwsgi.register_signal(86, "", checkproxy)
uwsgi.add_cron(86, 0, 9, -1, -1, -1)
uwsgi.register_signal(88, "", checkproxy)
uwsgi.add_cron(88, 0, 16, -1, -1, -1)
uwsgi.register_signal(90, "", migrateorder)
uwsgi.add_cron(90, 0, 0, -1, -1, -1)
