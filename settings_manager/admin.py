from django.contrib import admin
from django import forms

from .models import Banner, OfferStrip, SiteSettings, ShippingArea


COLOR_FIELDS = (

    # Typography & Body
    "body_bg_color",
    "body_text_color",
    "heading_color",
    "link_color",
    "link_hover_color",

    # Brand Colors
    "primary_color",
    "secondary_color",
    "accent_color",

    # Header
    "header_bg_color",
    "header_text_color",
    "header_nav_color",
    "header_nav_hover_color",
    "mobile_menu_icon_color",

    # Header Cart Button
    "header_cart_bg_color",
    "header_cart_text_color",
    "header_cart_hover_bg_color",

    # Global Body Buttons
    "body_button_bg_color",
    "body_button_text_color",
    "body_button_border_color",
    "body_button_hover_bg_color",
    "body_button_hover_text_color",

    # Footer
    "footer_bg_color",
    "footer_heading_color",
    "footer_text_color",
    "footer_link_color",
    "footer_link_hover_color",

    # Footer Social Icons
    "footer_social_icon_color",
    "footer_social_icon_hover_bg",
    "footer_social_icon_hover_text",

    # Banner
    "banner_text_color",
    "banner_button_text_color",
)


class SiteSettingsAdminForm(forms.ModelForm):

    class Meta:
        model = SiteSettings
        fields = "__all__"

        widgets = {
            field: forms.TextInput(
                attrs={
                    "type": "color",
                    "style": """
                        width: 75px;
                        height: 45px;
                        border-radius: 10px;
                        padding: 3px;
                        cursor: pointer;
                    """
                }
            )
            for field in COLOR_FIELDS
        }


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):

    form = SiteSettingsAdminForm

    fieldsets = (

        (
            "General Settings",
            {
                "fields": (
                    "site_name",
                    "font_family",
                    "email_enabled",
                ),
            },
        ),

        (
            "Typography & Body",
            {
                "fields": (
                    "body_bg_color",
                    "body_text_color",
                    "heading_color",
                    "link_color",
                    "link_hover_color",
                ),
                "description": (
                    "Controls overall body background, text colors, "
                    "headings, and links."
                ),
            },
        ),

        (
            "Brand Colors",
            {
                "fields": (
                    "primary_color",
                    "secondary_color",
                    "accent_color",
                ),
                "description": (
                    "Primary branding colors used throughout the site."
                ),
            },
        ),

        (
            "Header Settings",
            {
                "fields": (
                    "header_bg_color",
                    "header_text_color",
                    "header_nav_color",
                    "header_nav_hover_color",
                    "mobile_menu_icon_color",
                ),
                "description": (
                    "Controls navbar background, text, navigation links, "
                    "hover states, and mobile burger icon."
                ),
            },
        ),

        (
            "Header Cart Button",
            {
                "fields": (
                    "header_cart_bg_color",
                    "header_cart_text_color",
                    "header_cart_hover_bg_color",
                ),
                "description": (
                    "Separate styling for header cart button only."
                ),
            },
        ),

        (
            "Global Body Buttons",
            {
                "fields": (
                    "body_button_bg_color",
                    "body_button_text_color",
                    "body_button_border_color",
                    "body_button_hover_bg_color",
                    "body_button_hover_text_color",
                ),
                "description": (
                    "Controls ALL website buttons globally including "
                    "banner buttons, product buttons, add to cart, "
                    "checkout, forms, pagination, and action buttons."
                ),
            },
        ),

        (
            "Banner Settings",
            {
                "fields": (
                    "banner_text_color",
                    "banner_button_text_color",
                ),
                "description": (
                    "Controls banner title, subtitle, and button text colors."
                ),
            },
        ),

        (
            "Footer Settings",
            {
                "fields": (
                    "footer_bg_color",
                    "footer_heading_color",
                    "footer_text_color",
                    "footer_link_color",
                    "footer_link_hover_color",
                ),
                "description": (
                    "Controls footer background, text, headings, and links."
                ),
            },
        ),

        (
            "Footer Social Icons",
            {
                "fields": (
                    "footer_social_icon_color",
                    "footer_social_icon_hover_bg",
                    "footer_social_icon_hover_text",
                ),
                "description": (
                    "Controls footer social media icon colors and hover styles."
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
