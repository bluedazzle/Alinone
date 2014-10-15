from django.conf.urls import patterns, include, url
from django.contrib import admin
from CronOrder import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'AlinSite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^test/$', views.addtest),
)
