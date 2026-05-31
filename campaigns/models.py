from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse

from products.models import Product
from settings_manager.models import SEOFields


class Campaign(SEOFields):
    title = models.CharField(max_length=160)
    slug = models.SlugField(unique=True)
    banner_image = models.ImageField(
        upload_to="campaigns/",
        blank=True,
        null=True,
        help_text="Recommended: JPG, PNG, or WebP. Use a wide campaign banner around 1920x700px.",
    )
    offer_text = models.CharField(max_length=220, blank=True)
    discount_percentage = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Optional numeric discount badge shown on assigned product images. Example: enter 10 for 10% OFF.",
    )
    products = models.ManyToManyField(Product, blank=True, related_name="campaigns")
    is_active = models.BooleanField(default=True)
    starts_at = models.DateTimeField(blank=True, null=True)
    ends_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("campaigns:detail", args=[self.slug])
