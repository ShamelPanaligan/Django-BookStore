from django.contrib import admin
from .models import Book, Order, OrderItem

# Register the Book model to make it manageable through the Django admin
admin.site.register(Book)

# Define an inline admin interface for OrderItem to be displayed within Order admin
class OrderItemInline(admin.TabularInline):
    model = OrderItem  # Specifies the model to use in the inline

# Customize the admin interface for the Order model
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = ['id', 'user', 'email', 'paid', 'created_at']    
    list_filter = ['paid', 'created_at']
    search_fields = ['user__username', 'email']
    
    # Include related OrderItem instances directly in the Order detail view
    inlines = [OrderItemInline]
