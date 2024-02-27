# Generated by Django 5.0.2 on 2024-02-27 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page1', '0002_deliveryperson_package_vehicle_deliveryorder'),
    ]

    operations = [
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('start', models.DateTimeField(blank=True, null=True)),
                ('end', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='deliveryorder',
            name='delivery_person',
        ),
        migrations.RemoveField(
            model_name='deliveryorder',
            name='package',
        ),
        migrations.RemoveField(
            model_name='deliveryorder',
            name='vehicle',
        ),
        migrations.DeleteModel(
            name='DeliveryPerson',
        ),
        migrations.DeleteModel(
            name='Package',
        ),
        migrations.DeleteModel(
            name='DeliveryOrder',
        ),
        migrations.DeleteModel(
            name='Vehicle',
        ),
    ]
