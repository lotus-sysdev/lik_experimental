from django.db import models

# Create your models here.
class Report(models.Model):
    id = models.AutoField(primary_key=True)
    plat = models.CharField(max_length=20, null=True)
    driver = models.CharField(max_length=30, null=True)
    PO = models.CharField(max_length=40,  null=True)
    DO = models.CharField(max_length=7, null=True)
    no_tiket = models.CharField(max_length = 15, null=True)
    berat = models.PositiveIntegerField( null=True)
    tanggal = models.DateField( null=True)
    reject = models.PositiveIntegerField( null=True)