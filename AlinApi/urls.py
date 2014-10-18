from django.conf.urls import patterns, include, url
from AlinApi import views

urlpatterns = patterns('',
    url(r'^sender/bind_merchant$', views.bindmerchant),
    url(r'^sender/unbind_merchant$', views.unbindmerchant),
    url(r'^sender/bind_orders$', views.bindorders),
    url(r'^sender/finish_orders$', views.finishorder),
    url(r'^sender/gps_renew$', views.renewgps),
    url(r'^sender/info$', views.senderinfo),
    url(r'^$', views.testindex),
)

