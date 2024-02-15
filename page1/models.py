from django.db import models
import uuid
# Create your models here.
class Customer(models.Model):
    cust_id = models.IntegerField(primary_key=True)
    nama_pt = models.CharField(max_length=255)
    alamat_penagihan = models.CharField(max_length=255)
    alamat_pengiriman = models.CharField(max_length=255)
    telp = models.IntegerField()
    # pic = models.ForeignKey('PIC', on_delete=models.CASCADE, related_name='customers', null=True)
    terms_of_payment = models.IntegerField()
    pengiriman = models.BooleanField()
    npwp = models.CharField(max_length=255)
    faktur = models.BooleanField()

    def __str__(self):
        return str(self.id)