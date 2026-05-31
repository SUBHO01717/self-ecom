from django.contrib import admin

from .models import Color, Product, ProductImage, Size


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "sku", "price", "discount_price", "stock_quantity", "is_active", "is_featured", "is_new_arrival", "is_bestseller")
    list_filter = ("category", "is_active", "is_featured", "is_new_arrival", "is_bestseller", "is_campaign_product")
    list_editable = ("stock_quantity", "is_active", "is_featured", "is_new_arrival", "is_bestseller")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "sku", "short_description")
    filter_horizontal = ("sizes", "colors")
    inlines = [ProductImageInline]
    fieldsets = (
        ("Basic information", {"fields": ("category", "name", "slug", "sku", "short_description", "full_description", "thumbnail", "size_guide")}),
        ("Pricing and stock", {"fields": ("price", "discount_price", "stock_quantity", "is_active")}),
        ("Variants", {"fields": ("sizes", "colors")}),
        ("Labels", {"fields": ("is_featured", "is_new_arrival", "is_bestseller", "is_campaign_product")}),
        ("SEO", {"fields": ("seo_title", "meta_description", "meta_keywords", "og_image")}),
    )


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ("name", "display_order")
    list_editable = ("display_order",)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ("name", "hex_code")
