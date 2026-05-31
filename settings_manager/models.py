from pathlib import Path

from decimal import Decimal
from django.conf import settings
from django.core.validators import URLValidator
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


class Banner(models.Model):
    title = models.CharField(max_length=160)
    subtitle = models.CharField(max_length=255, blank=True)
    button_text = models.CharField(max_length=60, blank=True)
    button_url = models.CharField(
        max_length=255,
        blank=True,
        validators=[URLValidator(schemes=["http", "https"])],
        help_text="Use full absolute URLs starting with http:// or https://",
    )
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
    site_name = models.CharField(
        max_length=120,
        default="Daily Essentials"
    )

    # CSS customization fields were removed. Global presentation now relies on fixed defaults
    # in templates and static styles.

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

    cod_order_max_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Maximum order total allowed for Cash on Delivery. Set to 0 to allow COD for all orders.",
    )

    max_orders_per_phone_per_day = models.PositiveIntegerField(
        default=0,
        help_text="Maximum number of orders allowed per phone number in 24 hours. Set 0 to allow unlimited orders.",
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