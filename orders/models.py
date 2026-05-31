from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone

from products.models import Product


class PromoCode(models.Model):
    class DiscountType(models.TextChoices):
        PERCENT = "percent", "Percentage"
        FIXED = "fixed", "Fixed amount"

    code = models.CharField(max_length=40, unique=True, help_text="Customer-facing promo code. Example: FIRST10")
    description = models.CharField(max_length=180, blank=True)
    discount_type = models.CharField(max_length=20, choices=DiscountType.choices, default=DiscountType.PERCENT)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    minimum_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    maximum_discount_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Optional cap for percentage discounts.")
    is_active = models.BooleanField(default=True)
    starts_at = models.DateTimeField(blank=True, null=True)
    ends_at = models.DateTimeField(blank=True, null=True)
    usage_limit = models.PositiveIntegerField(blank=True, null=True, help_text="Optional total usage limit.")
    used_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return self.code

    def is_valid_for_subtotal(self, subtotal):
        now = timezone.now()
        if not self.is_active:
            return False, "This promo code is not active."
        if self.starts_at and self.starts_at > now:
            return False, "This promo code is not active yet."
        if self.ends_at and self.ends_at < now:
            return False, "This promo code has expired."
        if self.usage_limit is not None and self.used_count >= self.usage_limit:
            return False, "This promo code usage limit has been reached."
        if subtotal < self.minimum_order_amount:
            return False, f"Minimum order amount for this promo code is ৳{self.minimum_order_amount}."
        return True, ""

    def calculate_discount(self, subtotal):
        if self.discount_type == self.DiscountType.PERCENT:
            discount = subtotal * (self.discount_value / Decimal("100"))
            if self.maximum_discount_amount is not None:
                discount = min(discount, self.maximum_discount_amount)
        else:
            discount = self.discount_value
        return min(discount, subtotal).quantize(Decimal("0.01"))


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        PROCESSING = "processing", "Processing"
        SHIPPED = "shipped", "Shipped"
        DELIVERED = "delivered", "Delivered"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    class PaymentMethod(models.TextChoices):
        COD = "cod", "Cash on Delivery"
        BKASH = "bkash", "bKash Manual Payment"
        NAGAD = "nagad", "Nagad Manual Payment"

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name="orders")
    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    shipping_address = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.COD)
    transaction_id = models.CharField(max_length=120, blank=True)
    payment_verified = models.BooleanField(default=False)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    promo_code = models.CharField(max_length=40, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    purchase_pixel_pending = models.BooleanField(default=False)
    purchase_pixel_fired = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.pk}"

    def get_absolute_url(self):
        return reverse("orders:detail", args=[self.pk])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    product_name = models.CharField(max_length=180)
    sku = models.CharField(max_length=80)
    selected_size = models.CharField(max_length=60, blank=True)
    selected_color = models.CharField(max_length=60, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def line_total(self):
        if self.price is None or self.quantity is None:
            return Decimal("0.00")
        return self.price * self.quantity

    def __str__(self):
        return self.product_name
