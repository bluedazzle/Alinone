from django.conf.urls import patterns, include, url
from django.contrib import admin
<<<<<<< HEAD
import merchant_page.urls
from CronOrder import views
import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'AlinSite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^test/$', views.addtest),
    url(r'^merchant/', include(merchant_page.urls)),
    url(r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.CSS_DIR}),
    url(r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.JS_DIR}),
=======
from CronOrder import views
urlpatterns = patterns('',
    url(r'^api/v1/', include('AlinApi.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^test/$', views.addtest),
    url(r'^$', include('AlinApi.urls')),

>>>>>>> 30fc746ccc89d7064d9da3134a3e1ee06d056c10
)
