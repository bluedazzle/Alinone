from django.conf.urls import patterns, include, url
from AlinApi import views

urlpatterns = patterns('',
    url(r'^merchant/bind_merchant$', views.bindmerchant),
    url(r'^merchant/unbind_merchant$', views.unbindmerchant),
    url(r'^$', views.testindex),
)

