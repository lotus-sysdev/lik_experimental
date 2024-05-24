from django.core.management.base import BaseCommand
from lik.models import Report
from django.utils import timezone

import datetime

class Command(BaseCommand):
    help = 'Populate tiketId for existing Report instances'

    def handle(self, *args, **options):
        reports_without_tiketId = Report.objects.filter(tiketId__isnull=True)

        for report in reports_without_tiketId:
            sender_id_str = str(report.sender.pk).zfill(3)  # Use the sender ID, padded with leading zeros if needed
            
            current_date = report.date_time.strftime('%y%m')

            # Find the last tiketId for the current month and sender
            last_report = Report.objects.filter(
                sender=report.sender,
                tiketId__startswith=f"LIK{sender_id_str}{current_date}"
            ).order_by('-date_time').first()

            last_number = 0
            if last_report and last_report.tiketId:
                # Extract the base tiketId before any revisions (R[index])
                base_tiketId = last_report.tiketId.split('R', 1)[0]
                last_number_str = base_tiketId[-4:]
                if last_number_str.isdigit():
                    last_number = int(last_number_str)

            new_last_num = last_number + 1
            new_last_num = str(new_last_num).zfill(4)
            new_tiketId = f"LIK{sender_id_str}{current_date}{new_last_num}"

            report.tiketId = new_tiketId
            report.save()

        self.stdout.write(self.style.SUCCESS('Successfully populated tiketId for existing Report instances'))
