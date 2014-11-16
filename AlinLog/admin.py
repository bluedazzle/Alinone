from django.contrib import admin
from AlinLog.models import *
# Register your models here.

class CronLogAdmin(admin.ModelAdmin):
    list_display = ('ltype', 'content', 'status', 'err_message', 'log_time')
    ordering = ('-log_time',)
    list_filter = ('ltype', 'log_time',)


admin.site.register(CronLog, CronLogAdmin)
