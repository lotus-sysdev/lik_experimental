from django.db import models

# Create your models here.
class Report(models.Model):
    id = models.AutoField(primary_key=True)
    plat = models.CharField(max_length=20)
    driver = models.CharField(max_length=30)
    PO = models.CharField(max_length=40)
    DO = models.PositiveIntegerField()
    no_tiket = models.CharField(max_length = 15)
    berat = models.PositiveIntegerField()
    tanggal = models.DateField()
    reject = models.IntegerField()