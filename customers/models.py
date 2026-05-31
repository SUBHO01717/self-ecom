from django.conf import settings
from django.db import models


class CustomerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="customer_profile")
    phone = models.CharField(max_length=30, blank=True)
    shipping_address = models.TextField(blank=True)
    password_setup_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.get_full_name() or self.user.email or self.phone
