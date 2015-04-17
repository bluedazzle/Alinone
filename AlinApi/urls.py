from django.conf.urls import patterns, include, url
from AlinApi import views
from AlinApi import merhcant_api

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
    url(r'^sender/change_password$', views.changepasswd),
    url(r'^sender/forget_password$', views.forgetpasswd),
    url(r'^sender/new_password$', views.newpassword),
    url(r'^sender/req_verify$', views.reg_ver),
    url(r'^sender/get_bind_orders$', views.getcurlist),
    url(r'^sender/get_today_info$', views.send_info),
    url(r'^sender/get_pre_orders$', views.get_pending_order_num),
    #mercahnt api
    url(r'^merchant/login$', merhcant_api.login),
    url(r'^merchant/logout$', merhcant_api.logout),
    url(r'^merchant/register$', merhcant_api.register),
    url(r'^merchant/change_password$', merhcant_api.change_password),
    url(r'^merchant/change_info$', merhcant_api.change_info),
    url(r'^merchant/new_password$', merhcant_api.new_password),
    url(r'^merchant/get_verify$', merhcant_api.send_verify),
    url(r'^merchant/get_new$', merhcant_api.get_new_order),
    url(r'^merchant/get_new_detail$', merhcant_api.get_pending_order_detail),
    url(r'^merchant/ensure_order$', merhcant_api.ensure_order),
    url(r'^merchant/refuse_order$', merhcant_api.refuse_order),
    url(r'^merchant/create_order$', merhcant_api.create_new_order),
    url(r'^merchant/add_platform$', merhcant_api.add_platform),
    url(r'^merchant/delete_platform$', merhcant_api.delete_platform),
    url(r'^merchant/add_sender$', merhcant_api.add_sender),
    url(r'^merchant/delete_sender$', merhcant_api.delete_sender),
    url(r'^merchant/get_senders$', merhcant_api.get_senders),
    url(r'^merchant/get_handle_orders$', merhcant_api.get_handle_orders),
)

