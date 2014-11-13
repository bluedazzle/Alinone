from django.conf.urls import patterns, include, url
from django.contrib import admin
import merchant_page.urls
from CronOrder import views
import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'AlinSite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/', include('AlinApi.urls')),
    url(r'^$', include('merchant_page.urls')),
    url(r'^test/$', views.addtest),
    url(r'^merchant/', include(merchant_page.urls)),
    url(r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.CSS_DIR}),
    url(r'^img/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.IMG_DIR}),
    url(r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.JS_DIR}),
    url(r'^fonts/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.FONTS_DIR}),
    url(r'^dayin/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.DAYIN_DIR}),
    url(r'^qrimg/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.QR_DIR}),
    url(r'^music/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MUSIC_DIR}),
)
