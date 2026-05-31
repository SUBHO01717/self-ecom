from django.contrib import admin

from .models import Order, OrderItem, PromoCode


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "product_name", "sku", "selected_size", "selected_color", "quantity", "price", "line_total")
    can_delete = False


@admin.action(description="Mark selected orders as completed")
def mark_completed(modeladmin, request, queryset):
    queryset.update(status=Order.Status.COMPLETED, purchase_pixel_pending=True)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "phone", "status", "payment_method", "payment_verified", "subtotal", "shipping_cost", "discount_amount", "total", "created_at")
    list_filter = ("status", "payment_method", "payment_verified", "created_at", "shipping_area")
    list_editable = ("status", "payment_verified")
    search_fields = ("full_name", "phone", "email", "transaction_id", "promo_code")
    readonly_fields = ("subtotal", "promo_code", "discount_amount", "shipping_cost", "total", "purchase_pixel_pending", "purchase_pixel_fired", "created_at", "updated_at")
    inlines = [OrderItemInline]
    actions = [mark_completed]


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "discount_type", "discount_value", "minimum_order_amount", "is_active", "used_count", "usage_limit", "starts_at", "ends_at")
    list_filter = ("discount_type", "is_active")
    list_editable = ("is_active",)
    search_fields = ("code", "description")
