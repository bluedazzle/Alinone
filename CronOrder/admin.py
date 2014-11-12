from django.contrib import admin
from CronOrder.models import *
# Register your models here.

class MerchantAdmin(admin.ModelAdmin):
    list_display = ('name', 'alin_account', 'is_online')
    list_filter = ('last_login',)
    ordering = ('-last_login',)

class DayOrderAdmin(admin.ModelAdmin):
    list_display = ('order_id_alin', 'order_id_old', 'phone', 'pay', 'platform', 'real_price', 'status')
    list_filter = ('order_time',)
    ordering = ('-order_time',)

class DishAdmin(admin.ModelAdmin):
    list_display = ('dish_name', 'dish_count', 'dish_price', 'order')
    list_filter = ('dish_price',)
    ordering = ('-dish_name',)

class SenderAdmin(admin.ModelAdmin):
    list_display = ('phone', 'nick', 'update_time')
    list_filter = ('active_time',)
    ordering = ('-active_time',)


admin.site.register(Tdish, DishAdmin)
admin.site.register(TotalOrder, DayOrderAdmin)
admin.site.register(Merchant, MerchantAdmin)
admin.site.register(Dish, DishAdmin)
admin.site.register(DayOrder, DayOrderAdmin)
admin.site.register(Sender, SenderAdmin)