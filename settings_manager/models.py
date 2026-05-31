from pathlib import Path

from django.conf import settings
from django.db import models


def _convert_banner_to_web_image(image_field):
    if not image_field:
        return ""
    source = Path(image_field.path)
    if source.suffix.lower() not in {".tif", ".tiff"}:
        return image_field.url

    output_dir = Path(settings.MEDIA_ROOT) / "banners" / "rendered"
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / f"{source.stem}.jpg"
    if not output.exists() and source.exists():
        from PIL import Image

        with Image.open(source) as image:
            image.convert("RGB").save(output, "JPEG", quality=90, optimize=True)
    return f"{settings.MEDIA_URL}banners/rendered/{output.name}"


class SEOFields(models.Model):
    seo_title = models.CharField(max_length=160, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    og_image = models.ImageField(upload_to="seo/", blank=True, null=True)

    class Meta:
        abstract = True


# class SiteSettings(SEOFields):
#     class FontFamily(models.TextChoices):
#         INTER = "Inter, Arial, sans-serif", "Inter / Arial"
#         POPPINS = "Poppins, Arial, sans-serif", "Poppins"
#         ROBOTO = "Roboto, Arial, sans-serif", "Roboto"
#         LATO = "Lato, Arial, sans-serif", "Lato"
#         GEORGIA = "Georgia, serif", "Georgia"
#         SYSTEM = "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif", "System UI"

#     site_name = models.CharField(max_length=120, default="Daily Essentials")
#     font_family = models.CharField(
#         max_length=120,
#         choices=FontFamily.choices,
#         default=FontFamily.INTER,
#         help_text="Controls the main font family across the storefront.",
#     )
#     primary_color = models.CharField(max_length=7, default="#047857", help_text="Primary brand color. Example: #047857")
#     secondary_color = models.CharField(max_length=7, default="#0f172a", help_text="Secondary dark color. Example: #0f172a")
#     accent_color = models.CharField(max_length=7, default="#e11d48", help_text="Accent color for discount badges and highlights.")
#     body_bg_color = models.CharField(max_length=7, default="#f8fafc", help_text="Main page background color.")
#     text_color = models.CharField(max_length=7, default="#0f172a", help_text="Main text color.")
#     navbar_bg_color = models.CharField(max_length=7, default="#ffffff", help_text="Navbar background color.")
#     navbar_text_color = models.CharField(max_length=7, default="#0f172a", help_text="Header text color - controls the color of all text, icons, and links in the header/navbar.")
#     footer_bg_color = models.CharField(max_length=7, default="#ffffff", help_text="Footer background color.")
#     footer_text_color = models.CharField(max_length=7, default="#475569", help_text="Footer text color - controls the color of all text, icons, and links in the footer.")
#     button_bg_color = models.CharField(max_length=7, default="#047857", help_text="Main button background color.")
#     button_text_color = models.CharField(max_length=7, default="#ffffff", help_text="Main button text color.")
#     button_hover_bg_color = models.CharField(max_length=7, default="#065f46", help_text="Main button hover background color.")
#     link_color = models.CharField(max_length=7, default="#047857", help_text="Link and brand text color.")
#     facebook_pixel_id = models.CharField(max_length=80, blank=True)
#     google_analytics_id = models.CharField(max_length=80, blank=True)
#     custom_header_scripts = models.TextField(blank=True)
#     custom_footer_scripts = models.TextField(blank=True)
#     email_enabled = models.BooleanField(default=False)
#     facebook_url = models.URLField(blank=True)
#     instagram_url = models.URLField(blank=True)
#     tiktok_url = models.URLField(blank=True)
#     youtube_url = models.URLField(blank=True)
#     whatsapp_number = models.CharField(max_length=32, blank=True)

#     class Meta:
#         verbose_name = "Site settings"
#         verbose_name_plural = "Site settings"

#     def __str__(self):
#         return self.site_name

#     @classmethod
#     def load(cls):
#         obj, _created = cls.objects.get_or_create(pk=1)
#         return obj


class Banner(models.Model):
    title = models.CharField(max_length=160)
    subtitle = models.CharField(max_length=255, blank=True)
    button_text = models.CharField(max_length=60, blank=True)
    button_url = models.CharField(max_length=255, blank=True)
    background_image = models.ImageField(
        upload_to="banners/",
        help_text="Recommended: JPG, PNG, or WebP. Use a wide banner around 1920x700px. Avoid TIFF for browser display.",
    )
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "title"]

    def __str__(self):
        return self.title

    @property
    def display_image_url(self):
        return _convert_banner_to_web_image(self.background_image)


class OfferStrip(models.Model):
    text = models.CharField(max_length=180)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return self.text

class SiteSettings(SEOFields):
    class FontFamily(models.TextChoices):
        INTER = "Inter, Arial, sans-serif", "Inter / Arial"
        POPPINS = "Poppins, Arial, sans-serif", "Poppins"
        ROBOTO = "Roboto, Arial, sans-serif", "Roboto"
        LATO = "Lato, Arial, sans-serif", "Lato"
        GEORGIA = "Georgia, serif", "Georgia"
        SYSTEM = "system-ui, sans-serif", "System UI"

    site_name = models.CharField(
        max_length=120,
        default="Daily Essentials"
    )

    # =========================
    # Typography
    # =========================

    font_family = models.CharField(
        max_length=120,
        choices=FontFamily.choices,
        default=FontFamily.POPPINS,
    )

    body_bg_color = models.CharField(
        max_length=7,
        default="#f8fafc"
    )

    body_text_color = models.CharField(
        max_length=7,
        default="#0f172a"
    )

    heading_color = models.CharField(
        max_length=7,
        default="#0f172a"
    )

    link_color = models.CharField(
        max_length=7,
        default="#047857"
    )

    link_hover_color = models.CharField(
        max_length=7,
        default="#065f46"
    )

    # =========================
    # Header
    # =========================

    header_bg_color = models.CharField(
        max_length=7,
        default="#ffffff"
    )

    header_text_color = models.CharField(
        max_length=7,
        default="#0f172a"
    )

    header_nav_color = models.CharField(
        max_length=7,
        default="#0f172a"
    )

    header_nav_hover_color = models.CharField(
        max_length=7,
        default="#047857"
    )

    mobile_menu_icon_color = models.CharField(
        max_length=7,
        default="#0f172a"
    )

    # =========================
    # Header Cart Button
    # =========================

    header_cart_bg_color = models.CharField(
        max_length=7,
        default="#047857"
    )

    header_cart_text_color = models.CharField(
        max_length=7,
        default="#ffffff"
    )

    header_cart_hover_bg_color = models.CharField(
        max_length=7,
        default="#065f46"
    )

    # =========================
    # Global Body Buttons
    # =========================

    body_button_bg_color = models.CharField(
        max_length=7,
        default="#047857"
    )

    body_button_text_color = models.CharField(
        max_length=7,
        default="#ffffff"
    )

    body_button_border_color = models.CharField(
        max_length=7,
        default="#047857"
    )

    body_button_hover_bg_color = models.CharField(
        max_length=7,
        default="#065f46"
    )

    body_button_hover_text_color = models.CharField(
        max_length=7,
        default="#ffffff"
    )

    # =========================
    # Banner
    # =========================

    banner_text_color = models.CharField(
        max_length=7,
        default="#ffffff"
    )

    banner_button_text_color = models.CharField(
        max_length=7,
        default="#ffffff"
    )

    # =========================
    # Footer
    # =========================

    footer_bg_color = models.CharField(
        max_length=7,
        default="#ffffff"
    )

    footer_heading_color = models.CharField(
        max_length=7,
        default="#0f172a"
    )

    footer_text_color = models.CharField(
        max_length=7,
        default="#475569"
    )

    footer_link_color = models.CharField(
        max_length=7,
        default="#047857"
    )

    footer_link_hover_color = models.CharField(
        max_length=7,
        default="#065f46"
    )

    # =========================
    # Footer Social Icons
    # =========================

    footer_social_icon_color = models.CharField(
        max_length=7,
        default="#0f172a"
    )

    footer_social_icon_hover_bg = models.CharField(
        max_length=7,
        default="#047857"
    )

    footer_social_icon_hover_text = models.CharField(
        max_length=7,
        default="#ffffff"
    )

    # =========================
    # Product Details Page
    # =========================

    show_product_shipping_info = models.BooleanField(
        default=True,
        help_text="Show shipping and returns information on product detail pages"
    )

    show_free_shipping_info = models.BooleanField(
        default=True,
        help_text="Show 'Free shipping' message"
    )

    show_cash_on_delivery_info = models.BooleanField(
        default=True,
        help_text="Show 'Cash on delivery' message"
    )

    show_easy_returns_info = models.BooleanField(
        default=True,
        help_text="Show 'Easy returns' message"
    )

    # =========================
    # Brand Colors
    # =========================

    primary_color = models.CharField(
        max_length=7,
        default="#047857"
    )

    secondary_color = models.CharField(
        max_length=7,
        default="#0f172a"
    )

    accent_color = models.CharField(
        max_length=7,
        default="#e11d48"
    )

    # =========================
    # Tracking
    # =========================

    facebook_pixel_id = models.CharField(
        max_length=80,
        blank=True
    )

    google_analytics_id = models.CharField(
        max_length=80,
        blank=True
    )

    # =========================
    # Custom Scripts
    # =========================

    custom_header_scripts = models.TextField(blank=True)

    custom_footer_scripts = models.TextField(blank=True)

    # =========================
    # Social Links
    # =========================

    facebook_url = models.URLField(blank=True)

    instagram_url = models.URLField(blank=True)

    tiktok_url = models.URLField(blank=True)

    youtube_url = models.URLField(blank=True)

    whatsapp_number = models.CharField(
        max_length=32,
        blank=True
    )

    # =========================
    # Other
    # =========================

    email_enabled = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_name

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class ShippingArea(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="Example: Dhaka, Outside Dhaka")
    courier_fee = models.DecimalField(max_digits=10, decimal_places=2, help_text="Courier fee in ৳")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Shipping Area"
        verbose_name_plural = "Shipping Areas"

    def __str__(self):
        return f"{self.name} (৳{self.courier_fee})"