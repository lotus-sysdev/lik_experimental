from django.core.management.base import BaseCommand
from lik.models import Report
import datetime

class Command(BaseCommand):
    help = 'Populate tiketId for existing Report instances'

    def handle(self, *args, **options):
        reports_without_tiketId = Report.objects.filter(tiketId__isnull=True)

        for report in reports_without_tiketId:
            sender_id_str = str(report.sender.pk).zfill(3)  # Use the sender ID, padded with leading zeros if needed
            sender_code = report.sender.username[:3].upper()  # Take the first three letters of the sender's username

            last_report = Report.objects.filter(sender=report.sender).order_by('-date_time').first()

            if last_report and last_report.tiketId:
                last_number_str = last_report.tiketId[9:]  # Extract the index part of the last tiketId
                if last_number_str.isdigit():
                    last_number = int(last_number_str)
                else:
                    last_number = 0
            else:
                last_number = 0

            current_date = report.date_time.strftime('%y%m%d')

            new_index = last_number + 1
            new_tiketId = f"{current_date}{sender_id_str}{report.id}"
            report.tiketId = new_tiketId
            report.save()

        self.stdout.write(self.style.SUCCESS('Successfully populated tiketId for existing Report instances'))
