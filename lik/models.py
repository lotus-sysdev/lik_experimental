from django.db import models
from django.contrib.auth.models import User, Group


# Create your models here.
class Report(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)
    tiketId = models.CharField(max_length=100, null = True, blank = True)
    plat = models.CharField(max_length=20, null=True)
    driver = models.CharField(max_length=30, null=True)
    PO = models.CharField(max_length=40,  null=True)
    DO = models.CharField(max_length=20, null=True)
    lokasi = models.CharField(max_length=255, null = True)
    tujuan = models.CharField(max_length=255, null = True)
    kayu = models.CharField(max_length=255, null = True)
    no_tiket = models.CharField(max_length = 15, null=True)
    berat = models.PositiveIntegerField( null=True)
    #Tanggal Kirim
    tanggal = models.DateField( null=True)
    reject = models.PositiveIntegerField( null=True)
    completed = models.BooleanField(default=False, null=False)
    foto = models.ImageField(upload_to = 'report_photos/', null=True)
    og_foto = models.ImageField(upload_to = 'report_photos/', null=True, blank=True)
    #Timestamp
    date_time = models.DateTimeField(null = True)

    def __str__ (self):
        return str(self.no_tiket)

    def save(self, *args, **kwargs):
        if not self.tiketId:
            # Generate tiketId based on sender and a unique number
            if self.sender:
                sender_id_str = str(self.sender.pk).zfill(3)  # Use the sender ID, padded with leading zeros if needed

                current_date = self.date_time.strftime('%y%m')

                # Find the last tiketId for the current month and sender
                last_report = Report.objects.filter(
                    sender=self.sender,
                    tiketId__startswith=f"LIK{sender_id_str}{current_date}"
                ).order_by('-date_time').first()

                last_number = 0
                if last_report:
                    # Extract the base tiketId before any revisions (R[index])
                    base_tiketId = last_report.tiketId.split('R', 1)[0]
                    last_number = int(base_tiketId[-4:])
                
                new_last_num = last_number + 1
                new_last_num = str(new_last_num).zfill(4)
                new_tiketId = f"LIK{sender_id_str}{current_date}{new_last_num}"
                self.tiketId = new_tiketId

        super().save(*args, **kwargs)


class Lokasi(models.Model):
    class Meta:
        verbose_name = "Lokasi Potong"
        verbose_name_plural = "Lokasi Potong"
    nama = models.CharField(max_length=100)
    detail = models.SlugField(unique=True)

    def __str__(self):
        return self.nama

class Group_Lokasi(models.Model):
    class Meta:
        verbose_name = "Lokasi Group Access"
        verbose_name_plural = "Lokasi Group Access"
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    lokasi = models.ManyToManyField(Lokasi)

    def __str__(self):
        return str(self.group)
    
class Tujuan(models.Model):
    class Meta:
        verbose_name = "Pabrik Tujuan"
        verbose_name_plural = "Pabrik Tujuan"
    nama = models.CharField(max_length=100)
    detail = models.SlugField(unique=True)

    def __str__(self):
        return self.nama

class Group_Tujuan(models.Model):
    class Meta:
        verbose_name = "Tujuan Group Access"
        verbose_name_plural = "Tujuan Group Access"
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    tujuan = models.ManyToManyField(Tujuan)

    def __str__(self):
        return str(self.group)

class Kayu(models.Model):
    class Meta:
        verbose_name = "Kayu"
        verbose_name_plural = "Jenis Kayu"
    nama = models.CharField(max_length=100)
    detail = models.SlugField(unique=True)

    def __str__(self):
        return self.nama

class Group_Kayu(models.Model):
    class Meta:
        verbose_name = "Kayu Group Access"
        verbose_name_plural = "Kayu Group Access"
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    kayu = models.ManyToManyField(Kayu)

    def __str__(self):
        return str(self.group)
