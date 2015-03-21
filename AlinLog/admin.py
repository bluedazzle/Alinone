from django.contrib import admin
from AlinLog.models import *
# Register your models here.

class CronLogAdmin(admin.ModelAdmin):
    list_display = ('ltype', 'content', 'status', 'err_message', 'log_time')
    ordering = ('-log_time',)
    list_filter = ('ltype', 'log_time',)

class RunTimeLogAdmin(admin.ModelAdmin):
    list_display = ('merchant', 'ltype', 'content', 'status', 'err_message', 'log_time')
    ordering = ('-log_time', 'merchant',)
    list_filter = ('ltype', 'log_time', 'merchant',)

class AccountLogAdmin(admin.ModelAdmin):
    list_display = ('account', 'atype', 'ltype', 'note', 'content', 'log_time')
    ordering = ('-log_time', 'account',)
    list_filter = ('ltype', 'log_time', 'account',)

class SearchLogAdmin(admin.ModelAdmin):
    list_display = ('req_ip', 'req_param', 'req_time')
    ordering = ('-req_time', 'req_ip',)
    list_filter = ('req_time', 'req_ip',)


class ProRunTimeLogAdmin(admin.ModelAdmin):
    list_display = ('error_file', 'error_line', 'log_time')
    ordering = ('-log_time', 'error_file',)
    list_filter = ('error_file',)


admin.site.register(CronLog, CronLogAdmin)
admin.site.register(RunTimeLog, RunTimeLogAdmin)
admin.site.register(AccountLog, AccountLogAdmin)
admin.site.register(SeachLog, SearchLogAdmin)
admin.site.register(ProRunTimeLog, ProRunTimeLogAdmin)