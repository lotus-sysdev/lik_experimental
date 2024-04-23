# your_app/management/commands/import_data.py

import csv
from django.core.management.base import BaseCommand
from page1.models import Provinsi, Kota, Kecamatan, Kelurahan
import os

class Command(BaseCommand):
    help = 'Import data from CSV files'

    def add_arguments(self, parser):
        parser.add_argument('csv_folder', type=str, help='Path to the folder containing CSV files')

    def handle(self, *args, **options):
        csv_folder_path = options['csv_folder']
        province_file_path = os.path.join(csv_folder_path, 'provinsi.csv')
        regency_file_path = os.path.join(csv_folder_path, 'kota.csv')
        district_file_path = os.path.join(csv_folder_path, 'kecamatan.csv')
        village_file_path = os.path.join(csv_folder_path, 'kelurahan.csv')

        self.import_provinces(province_file_path)
        self.import_regencies(regency_file_path)
        self.import_districts(district_file_path)
        self.import_villages(village_file_path)

    def import_provinces(self, file_path):
        with open(file_path, 'r', encoding='utf-8-sig') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                province_id = row[0]
                province_name = row[1]
                province, _ = Provinsi.objects.get_or_create(id = province_id, name=province_name)
                self.stdout.write(f"Imported Province: {province}")

    def import_regencies(self, file_path):
        with open(file_path, 'r', encoding='utf-8-sig') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                regency_id = row[0]
                province_id = row[1]
                provinsi_id = Provinsi.objects.get(id=province_id)
                regency_name = row[2]
                regency, _ = Kota.objects.get_or_create(id = regency_id, provinsi_id=provinsi_id, name=regency_name)
                self.stdout.write(f"Imported Regency: {regency}")

    def import_districts(self, file_path):
        with open(file_path, 'r', encoding='utf-8-sig') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                district_id = row[0]
                regency_id = row[1]  # Assuming the CSV contains regency names
                kota_id = Kota.objects.get(id=regency_id)
                district_name = row[2]
                district, _ = Kecamatan.objects.get_or_create(id = district_id, kota_id=kota_id, name=district_name)
                self.stdout.write(f"Imported District: {district}")

    def import_villages(self, file_path):
        with open(file_path, 'r', encoding='utf-8-sig') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                village_id = row[0]
                district_id = row[1]
                kecamatan_id = Kecamatan.objects.get(id=district_id)
                village_name = row[2]
                village, _ = Kelurahan.objects.get_or_create(id = village_id, kecamatan_id=kecamatan_id, name=village_name)
                self.stdout.write(f"Imported Village: {village}")
