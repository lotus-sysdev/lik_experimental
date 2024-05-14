from django.db import models
from django.contrib.auth.models import User, Group
import datetime

# Create your models here.
class Report(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)
    tiketId = models.CharField(max_length=100, null = True, blank = True)
    plat = models.CharField(max_length=20, null=True)
    driver = models.CharField(max_length=30, null=True)
    PO = models.CharField(max_length=40,  null=True)
    DO = models.CharField(max_length=7, null=True)
    lokasi = models.CharField(max_length=255, null = True)
    tujuan = models.CharField(max_length=255, null = True)
    kayu = models.CharField(max_length=255, null = True)
    no_tiket = models.CharField(max_length = 15, null=True)
    berat = models.PositiveIntegerField( null=True)
    #Tanggal Kirim
    tanggal = models.DateField( null=True)
    reject = models.PositiveIntegerField( null=True)
    foto = models.ImageField(upload_to = 'report_photos/', null=True)
    og_foto = models.ImageField(upload_to = 'report_photos/', null=True)
    #Timestamp
    date_time = models.DateTimeField(null = True)

    def __str__ (self):
        return str(self.no_tiket)

    def save(self, *args, **kwargs):
        if not self.tiketId:
            # Generate tiketId based on sender and a unique number
            if self.sender:
                sender_id_str = str(self.sender.pk).zfill(3)  # Use the sender ID, padded with leading zeros if needed
                # sender_code = self.sender.username[:3].upper()  # Take the first three letters of the sender's username

                # Retrieve the last tiketId for the same sender
                last_report = Report.objects.filter(sender=self.sender).order_by('-date_time').first()
                last_number = 0
                if last_report and last_report.id:
                    last_number = last_report.id
                else:
                    last_number = 0

                current_date = self.date_time.strftime('%y%m%d')
                
                new_last_num = last_number + 1
                new_tiketId = f"{current_date}{sender_id_str}{new_last_num}"  # Combine date, sender ID, and a 3-digit number
                self.tiketId = new_tiketId

        super().save(*args, **kwargs)


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

class Kayu(models.Model):
    nama = models.CharField(max_length=100)
    detail = models.SlugField(unique=True)

    def __str__(self):
        return self.nama

class Group_Kayu(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    kayu = models.ManyToManyField(Kayu)

    def __str__(self):
        return str(self.group)