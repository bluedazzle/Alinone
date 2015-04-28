from django.contrib import admin
from CronOrder.models import *
# Register your models here.

class MerchantAdmin(admin.ModelAdmin):
    list_display = ('name', 'alin_account', 'belongs', 'is_online')
    list_filter = ('last_login',)
    search_fields = ('alin_account', 'name')
    ordering = ('-last_login',)

class DayOrderAdmin(admin.ModelAdmin):
    list_display = ('order_id_alin', 'merchant', 'order_time', 'order_id_old', 'phone', 'pay', 'platform', 'real_price', 'status')
    list_filter = ('order_time', 'merchant',)
    search_fields = ('order_id_alin', 'merchant__alin_account', 'phone')
    ordering = ('-order_id_alin',)

class DishAdmin(admin.ModelAdmin):
    list_display = ('dish_name', 'dish_count', 'dish_price', 'order')
    list_filter = ('dish_price',)
    ordering = ('-dish_name',)

class SenderAdmin(admin.ModelAdmin):
    list_display = ('phone', 'belongs', 'nick', 'update_time')
    list_filter = ('active_time',)
    ordering = ('-active_time',)


admin.site.register(Tdish, DishAdmin)
admin.site.register(TotalOrder, DayOrderAdmin)
admin.site.register(Merchant, MerchantAdmin)
admin.site.register(Dish, DishAdmin)
admin.site.register(DayOrder, DayOrderAdmin)
admin.site.register(Sender, SenderAdmin)
admin.site.register(CatcheData)