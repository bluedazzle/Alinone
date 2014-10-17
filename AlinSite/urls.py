from django.conf.urls import patterns, include, url
from django.contrib import admin
from CronOrder import views
urlpatterns = patterns('',
    url(r'^api/v1/', include('AlinApi.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^test/$', views.addtest),
    url(r'^$', include('AlinApi.urls')),

)
