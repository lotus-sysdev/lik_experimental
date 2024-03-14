from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import CustomerAlamat, SupplierAlamat, DeliveryAddresses

@receiver(post_save, sender=CustomerAlamat)
@receiver(post_save, sender=SupplierAlamat)
@receiver(post_delete, sender=CustomerAlamat)
@receiver(post_delete, sender=SupplierAlamat)
def update_delivery_addresses(sender, instance, **kwargs):
    if isinstance(instance, CustomerAlamat) or isinstance(instance, SupplierAlamat):
        # Check if the instance is being created or deleted
        if kwargs.get('created', False):
            # Create DeliveryAddresses instance
            DeliveryAddresses.objects.create(
                provinsi=instance.provinsi,
                kota=instance.kota,
                kecamatan=instance.kecamatan,
                kelurahan=instance.kelurahan,
                detail=instance.detail
            )
        else:
            # Delete DeliveryAddresses instance if it exists
            DeliveryAddresses.objects.filter(
                provinsi=instance.provinsi,
                kota=instance.kota,
                kecamatan=instance.kecamatan,
                kelurahan=instance.kelurahan,
                detail=instance.detail
            ).delete()
