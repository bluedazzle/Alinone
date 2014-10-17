from django.conf.urls import patterns, include, url
from AlinApi import views

urlpatterns = patterns('',
    url(r'^merchant/bind_merchant$', views.bindMerchant),
    url(r'^$', views.testindex),
)

