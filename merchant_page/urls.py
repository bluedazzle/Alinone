from django.conf.urls import patterns, include, url
from views import *
from operate_detail import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Alinone.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^login_in$', login_in),
    url(r'^$', login_in),
    url(r'^login_in$',  login_in),
    url(r'^login_out$', login_out),
    url(r'^register$', register),
    url(r'^register_verify', register_verify),
    url(r'^forget_password', forget_password),
    url(r'^change_password', change_password),
    # url(r'^login_ver', login_ver),
    # only for test
    url(r'^fuwei$', fuwei),

    url(r'^operate_new$', operate_new),
    url(r'^operate_get$', operate_get),
    url(r'^operate_paisong$', operate_paisong),
    url(r'^operate_pingtai$', operate_pingtai),
    url(r'^operate_delete$', operate_delete),
    url(r'^operate_express_person$', operate_express_person),
    url(r'^printer_setting$', printer_setting),
    url(r'^jieshouone(?P<order>.*)$', jieshouone),
    url(r'^jujueone(?P<order>.*)$', jujueone),
    url(r'^print_one(?P<order>.*)$', print_one),
    url(r'^platform_delete(?P<name>.*)$', platform_delete),
    url(r'^add_platform_page$', add_platform_page),
    url(r'^add_platform$', add_platform),
    url(r'^delete_sender(?P<phone>.*)$', delete_sender),
    url(r'^add_sender_page$', add_sender_page),
    url(r'^print_all$', print_all),
    url(r'^jujueall$', jujueall),
    url(r'^jieshouall$', jieshouall),
)
