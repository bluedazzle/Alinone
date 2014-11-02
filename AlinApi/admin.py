from django.contrib import admin
from AlinApi.models import *
# Register your models here.

class PhoneVerifyAdmin(admin.ModelAdmin):
    list_display = ('phone', 'verify_code', 'update_time')
    list_filter = ('update_time',)
    ordering = ('-update_time',)

admin.site.register(PhoneVerify, PhoneVerifyAdmin)