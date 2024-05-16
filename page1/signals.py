from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import CustomerAlamat, SupplierAlamat, DeliveryAddresses, Items, ItemChangeLog
from .middleware import get_current_user


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

@receiver(pre_save, sender=Items)
def log_item_update(sender, instance, **kwargs):
    user = get_current_user()
    if instance.pk:
        try:
            old_instance = Items.objects.get(pk=instance.pk)
        except Items.DoesNotExist:
            old_instance=None

        if old_instance:
            for field in instance._meta.fields:

                if field.name != 'SKU':
                    old_value = getattr(old_instance, field.name)
                    new_value = getattr(instance, field.name)

                    # print(f"Field: {field.name}, Old value: {old_value}, New value: {new_value}")

                    if old_value != new_value:
                        # print(f"User: {user}")
                        field_name = instance._meta.get_field(field.name).verbose_name

                        ItemChangeLog.objects.create(
                            item=instance,
                            user=user,
                            field_changed=field_name,
                            old_value=old_value,
                            new_value=new_value
                        )
