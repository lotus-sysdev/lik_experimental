# myapp/management/commands/import_kodepos.py
import csv
from django.core.management.base import BaseCommand
from page1.models import KodePos, Kelurahan  # Import your models


class Command(BaseCommand):
    help = 'Import data from a CSV file into the KodePos model'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            for row in reader:
                kode_pos = row[0]
                kelurahan_id = row[1]
                
                # Fetch the Kecamatan object
                try:
                    kelurahan = Kelurahan.objects.get(id=kelurahan_id)
                except Kelurahan.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Kelurahan with ID {kelurahan_id} does not exist. Skipping...'))
                    continue
                
                # Create or update KodePos object
                try:
                    kodepos_obj, created = KodePos.objects.update_or_create(
                        kode_pos=kode_pos,
                        kelurahan_id=kelurahan
                    )
                    if created:
                        # self.stdout.write(self.style.SUCCESS(f'Successfully created KodePos {kode_pos}'))
                        pass
                    else:
                        # self.stdout.write(self.style.SUCCESS(f'Successfully updated KodePos {kode_pos}'))
                        pass
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error creating/updating KodePos {kode_pos}: {str(e)}'))
