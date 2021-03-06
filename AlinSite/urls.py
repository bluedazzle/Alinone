from django.conf.urls import patterns, include, url
from django.contrib import admin
import merchant_page.urls
import Alin_admin.urls
from CronOrder import views
import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'AlinSite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^adminmkjbalinone/', include(admin.site.urls)),
    url(r'^api/v1/', include('AlinApi.urls')),
    url(r'^$', include('merchant_page.urls')),
    url(r'^test/$', views.addtest),
    url(r'^merchant/', include(merchant_page.urls)),
    url(r'^alin_admin/', include(Alin_admin.urls)),
    url(r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.CSS_DIR}),
    url(r'^img/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.IMG_DIR}),
    url(r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.JS_DIR}),
    url(r'^fonts/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.FONTS_DIR}),
    url(r'^dayin/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.DAYIN_DIR}),
    url(r'^qrimg/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.QR_DIR}),
    url(r'^music/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MUSIC_DIR}),
    url(r'^apk/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.APK_DIR}),
)


# if settings.DEBUG:
#         import debug_toolbar
#         urlpatterns += patterns('',
#             url(r'^__debug__/', include(debug_toolbar.urls)),
#         )