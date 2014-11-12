import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SeaSite.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
