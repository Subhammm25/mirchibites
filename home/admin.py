from django.contrib import admin
from .models import Product
from .models import Order
from .models import OrderItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'created_at')
    search_fields = ('name',)


# Register the Order model to the admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email', 'status', 'total_price', 'created_at')
    search_fields = ('name', 'phone', 'email')
    list_filter = ('status', 'created_at')
    
    
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('product__name',)    