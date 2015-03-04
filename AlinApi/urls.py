from django.conf.urls import patterns, include, url
from AlinApi import views

urlpatterns = patterns('',
    url(r'^sender/bind_merchant$', views.bindmerchant),
    url(r'^sender/unbind_merchant$', views.unbindmerchant),
    url(r'^sender/bind_orders$', views.bindorders),
    url(r'^sender/finish_orders$', views.finishorder),
    url(r'^sender/gps_renew$', views.renewgps),
    url(r'^sender/info$', views.senderinfo),
    url(r'^sender/login$', views.login),
    url(r'^sender/register$', views.register),
    url(r'^website/search$', views.searchmeal),
    url(r'^$', views.testindex),
    url(r'^sender/change_password$', views.changepasswd),
    url(r'^sender/forget_password$', views.forgetpasswd),
    url(r'^sender/new_password$', views.newpassword),
    url(r'^sender/req_verify$', views.reg_ver),
    url(r'^sender/get_bind_orders$', views.getcurlist),
    url(r'^sender/get_today_info', views.send_info),
)

