from django.db import models
from django.urls import reverse

from settings_manager.models import SEOFields


class Category(SEOFields):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    image = models.ImageField(
        upload_to="categories/",
        blank=True,
        null=True,
        help_text="Recommended: square JPG, PNG, or WebP image, at least 600x600px.",
    )
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    show_on_home = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("categories:products", args=[self.slug])
