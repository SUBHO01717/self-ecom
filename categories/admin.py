from django.contrib import admin

from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "show_on_home", "display_order")
    list_editable = ("is_active", "show_on_home", "display_order")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description")
    fieldsets = (
        (None, {"fields": ("name", "slug", "image", "description", "is_active", "show_on_home", "display_order")}),
        ("SEO", {"fields": ("seo_title", "meta_description", "meta_keywords", "og_image")}),
    )
