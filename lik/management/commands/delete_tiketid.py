from django.core.management.base import BaseCommand
from lik.models import Report

class Command(BaseCommand):
    help = 'Delete tiketId for every Report instance'

    def handle(self, *args, **options):
        reports = Report.objects.all()
        for report in reports:
            report.tiketId = None
            report.save()

        self.stdout.write(self.style.SUCCESS('Successfully deleted tiketId for all Report instances'))
