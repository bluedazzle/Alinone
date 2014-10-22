from django.conf.urls import patterns, include, url
from views import *
from operate_detail import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Alinone.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^login_in$', login_in),
    url(r'^login_in$',  login_in),
    url(r'^login_out$', login_out),
    url(r'^register$', register),
    # url(r'^login_ver', login_ver),
    # only for test
    url(r'^fuwei$', fuwei),

    url(r'^operate_new$', operate_new),
    url(r'^operate_get$', operate_get),
    url(r'^operate_paisong$', operate_paisong),
    url(r'^operate_pingtai$', operate_pingtai),
    url(r'^operate_delete$', operate_delete),
    url(r'^operate_express_person$', operate_express_person),
    url(r'^jieshouone(?P<order>.*)$', jieshouone),
    url(r'^jujueone(?P<order>.*)$', jujueone),
    url(r'^jujueall$', jujueall),
    url(r'^jieshouall$', jieshouall),
)
