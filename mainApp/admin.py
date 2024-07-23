from django.contrib import admin

# Register your models here.
from .models import Category, Tag, Product, Review, Order, OrderItem

admin.site.register(Category)
admin.site.register(Tag)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'category', 'created_at', 'updated_at')
    search_fields = ('name', 'description', 'category__name')
    list_filter = ('category', 'created_at', 'updated_at')
admin.site.register(Product, ProductAdmin)
# admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(OrderItem)

