from django.conf.urls import patterns, include, url
from views import *


urlpatterns = patterns('',
                       url(r'^admin_login$', login),
                       url(r'^admin_host$', alin_admin_host),
                       url(r'^update_count$', count),
                       url(r'^merchant_verify$', verify_merchant),
                       url(r'^merchant_list$', merchant_list),
                       url(r'^manage_log$', manage_log),
                       url(r'^logout$', logout),
                       url(r'^account_log$', account_log),
                       url(r'^pro_run_time_log$', pro_run_time_log),
                       url(r'^run_time_log$', run_time_log),
                       url(r'^cron_log$', cron_log),
                       url(r'seach_log$', seach_log),

                       # option
                       url(r'^pass_merchant$', pass_merchant),
                       url(r'^reject_merchant$', reject_merchant),
                       # test
                       url(r'create_order$', create_order),
                       )