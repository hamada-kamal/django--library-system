from django.contrib import admin
from .models import *


class orderLineItem(admin.TabularInline):
    model = OrderLine
    extra = 0

class QuiqorderLineItem(admin.TabularInline):
    model = QuiqOrderLine
    extra = 0
    
class OrderAdmin(admin.ModelAdmin):
    
    list_display = ('client','transaction_id','complete','date_ordered','remaining_atthattime','paid')
    inlines = [orderLineItem]



class QuiqOrderAdmin(admin.ModelAdmin):

    list_display = ('transaction_id','complete','date','paid')
    inlines = [QuiqorderLineItem]

admin.site.register(Product)
admin.site.register(Client)
admin.site.register(Order, OrderAdmin)
admin.site.register(QuiqOrder, QuiqOrderAdmin)
admin.site.register(OrderLine)
