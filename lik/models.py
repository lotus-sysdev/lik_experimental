from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.
class Report(models.Model):
    id = models.AutoField(primary_key=True)
    plat = models.CharField(max_length=20, null=True)
    driver = models.CharField(max_length=30, null=True)
    PO = models.CharField(max_length=40,  null=True)
    DO = models.CharField(max_length=7, null=True)
    lokasi = models.CharField(max_length=255, null = True)
    tujuan = models.CharField(max_length=255, null = True)
    no_tiket = models.CharField(max_length = 15, null=True)
    berat = models.PositiveIntegerField( null=True)
    tanggal = models.DateField( null=True)
    reject = models.PositiveIntegerField( null=True)
    foto = models.BinaryField(null=True, blank=True)

    def __str__ (self):
        return str(self.no_tiket)

class Lokasi(models.Model):
    nama = models.CharField(max_length=100)
    detail = models.SlugField(unique=True)

    def __str__(self):
        return self.nama

class Group_Lokasi(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    lokasi = models.ManyToManyField(Lokasi)

    def __str__(self):
        return str(self.group)
    
class Tujuan(models.Model):
    nama = models.CharField(max_length=100)
    detail = models.SlugField(unique=True)

    def __str__(self):
        return self.nama

class Group_Tujuan(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    tujuan = models.ManyToManyField(Tujuan)

    def __str__(self):
        return str(self.group)
