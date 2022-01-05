from django.contrib import admin
from .models import *
# Register your models here.

class orderLineItem(admin.TabularInline):
    model = OrderItem
    # readonly_fields = ['product','quantity',]
    extra = 0
class OrderAdmin(admin.ModelAdmin):
    # fields = (('customer' ,'complete',),'transaction_id')

    list_display = ('client','transaction_id','complete','date_ordered',)
    # readonly_fields = ['customer','complete','transaction_id']
    # list_filter = ('complete',)
    inlines = [orderLineItem]

admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Client)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)