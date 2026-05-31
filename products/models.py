from django.db import models
from django.urls import reverse
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field

from categories.models import Category
from settings_manager.models import SEOFields


class ProductQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True).select_related("category")

    def in_stock(self):
        return self.filter(stock_quantity__gt=0)


class Size(models.Model):
    name = models.CharField(max_length=60, unique=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "name"]

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=60, unique=True)
    hex_code = models.CharField(max_length=7, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(SEOFields):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    name = models.CharField(max_length=180)
    slug = models.SlugField(unique=True)
    short_description = models.CharField(max_length=255, blank=True)
    full_description = CKEditor5Field("Full Description",config_name="default",blank=True,null=True,help_text="Detailed product description with rich text formatting.")
    sku = models.CharField(max_length=80, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    thumbnail = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True,
        help_text="Recommended: square JPG, PNG, or WebP product image, at least 800x800px.",
    )
    size_guide = models.ImageField(
        upload_to="size-guides/",
        blank=True,
        null=True,
        help_text="Optional. Upload a clear JPG, PNG, or WebP size guide image.",
    )
    sizes = models.ManyToManyField(Size, blank=True)
    colors = models.ManyToManyField(Color, blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    is_campaign_product = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ProductQuerySet.as_manager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    @property
    def current_price(self):
        campaign_price = None
        campaign_discount = self.campaign_discount_percentage
        if campaign_discount:
            campaign_price = self.price - (self.price * campaign_discount / 100)

        prices = [self.price]
        if self.discount_price and self.discount_price < self.price:
            prices.append(self.discount_price)
        if campaign_price and campaign_price < self.price:
            prices.append(campaign_price)
        return min(prices).quantize(self.price)

    @property
    def discount_percentage(self):
        if self.discount_price and self.price and self.discount_price < self.price:
            return round(((self.price - self.discount_price) / self.price) * 100)
        return 0

    @property
    def campaign_discount_percentage(self):
        now = timezone.now()
        campaigns = self.campaigns.filter(is_active=True, discount_percentage__gt=0).filter(
            models.Q(starts_at__isnull=True) | models.Q(starts_at__lte=now),
            models.Q(ends_at__isnull=True) | models.Q(ends_at__gte=now),
        )
        return campaigns.order_by("-discount_percentage").values_list("discount_percentage", flat=True).first() or 0

    @property
    def display_discount_percentage(self):
        return max(self.discount_percentage, self.campaign_discount_percentage)

    @property
    def has_active_discount(self):
        return self.current_price < self.price

    def get_absolute_url(self):
        return reverse("products:detail", args=[self.slug])


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="gallery")
    image = models.ImageField(
        upload_to="products/gallery/",
        help_text="Recommended: JPG, PNG, or WebP image matching the main product image ratio.",
    )
    alt_text = models.CharField(max_length=160, blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return f"{self.product.name} image"
