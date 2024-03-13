from .models import *
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=CustomerAlamat)
@receiver(post_save, sender=SupplierAlamat)
def update_delivery_addresses(sender, instance, created, **kwargs):
    if created:
        # Create DeliveryAddresses instance
        DeliveryAddresses.objects.create(
            provinsi=instance.provinsi,
            kota=instance.kota,
            kecamatan=instance.kecamatan,
            kelurahan=instance.kelurahan,
            detail=instance.detail
        )