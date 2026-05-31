from django.contrib import admin

from .models import Banner, OfferStrip, SiteSettings, ShippingArea


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):

    fieldsets = (

        (
            "General Settings",
            {
                "fields": (
                    "site_name",
                    "email_enabled",
                ),
            },
        ),

        (
            "Product Details Page",
            {
                "fields": (
                    "show_product_shipping_info",
                    "show_free_shipping_info",
                    "show_cash_on_delivery_info",
                    "show_easy_returns_info",
                ),
                "description": (
                    "Enable or disable shipping information display on product detail pages."
                ),
            },
        ),

        (
            "Payment Settings",
            {
                "fields": (
                    "cod_order_max_amount",
                    "max_orders_per_phone_per_day",
                ),
                "description": (
                    "Control Cash on Delivery order limits and how many orders one customer can place in a day."
                ),
            },
        ),

        (
            "SEO Settings",
            {
                "fields": (
                    "seo_title",
                    "meta_description",
                    "meta_keywords",
                    "og_image",
                ),
            },
        ),

        (
            "Tracking & Scripts",
            {
                "fields": (
                    "facebook_pixel_id",
                    "google_analytics_id",
                    "custom_header_scripts",
                    "custom_footer_scripts",
                ),
            },
        ),

        (
            "Social Media",
            {
                "fields": (
                    "facebook_url",
                    "instagram_url",
                    "tiktok_url",
                    "youtube_url",
                    "whatsapp_number",
                ),
            },
        ),

    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "is_active",
        "display_order",
    )

    list_editable = (
        "is_active",
        "display_order",
    )

    search_fields = (
        "title",
        "subtitle",
    )


@admin.register(OfferStrip)
class OfferStripAdmin(admin.ModelAdmin):

    list_display = (
        "text",
        "is_active",
        "display_order",
    )

    list_editable = (
        "is_active",
        "display_order",
    )

    search_fields = (
        "text",
    )


@admin.register(ShippingArea)
class ShippingAreaAdmin(admin.ModelAdmin):
    list_display = ("name", "courier_fee", "is_active", "created_at")
    list_editable = ("courier_fee", "is_active")
    search_fields = ("name",)
    list_filter = ("is_active",)
