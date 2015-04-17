from django.conf.urls import patterns, include, url
from views import *


urlpatterns = patterns('',
                       url(r'^admin_login$', login))