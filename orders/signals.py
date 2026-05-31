from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Order


@receiver(pre_save, sender=Order)
def queue_purchase_pixel_after_completion(sender, instance, **kwargs):
    if not instance.pk or instance.status != Order.Status.COMPLETED:
        return
    old_status = sender.objects.filter(pk=instance.pk).values_list("status", flat=True).first()
    if old_status != Order.Status.COMPLETED:
        instance.purchase_pixel_pending = True
