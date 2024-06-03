from django.core.management.base import BaseCommand
from lik.models import Report

class Command(BaseCommand):
    help = 'Delete tiketId for every Report instance'

    def handle(self, *args, **options):
        try:
            reports = Report.objects.all()
            self.stdout.write(f'Number of reports found: {reports.count()}')
            
            reports.update(tiketId=None)
            self.stdout.write(self.style.SUCCESS('Successfully deleted tiketId for all Report instances'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))