from django.contrib import admin
from ProxyWork.models import *
# Register your models here.

class ProxyAdmin(admin.ModelAdmin):
    list_display = ('ip', 'get_time', 'is_used', 'is_online')
    list_filter = ('get_time',)
    ordering = ('-get_time',)

admin.site.register(Proxy, ProxyAdmin)
