from django.contrib import admin

from .models import Campaign


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ("title", "discount_percentage", "is_active", "starts_at", "ends_at")
    list_editable = ("is_active",)
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("products",)
    fieldsets = (
        (None, {"fields": ("title", "slug", "banner_image", "offer_text", "discount_percentage", "products", "is_active", "starts_at", "ends_at")}),
        ("SEO", {"fields": ("seo_title", "meta_description", "meta_keywords", "og_image")}),
    )
