from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from page1.models import Prospect, ProspectTicket
from django.conf import settings
from django.db.models import Subquery, OuterRef

class Command(BaseCommand):
    help = 'Sends reminder emails for prospects that have not been updated by in_charge'

    def handle(self, *args, **kwargs):
        # Define the reminder periods
        reminder_periods = [3, 7, 14, 30]  # Days

        for period in reminder_periods:
            # Calculate the date for the reminder
            reminder_date = timezone.now() - timezone.timedelta(days=period)

            # Subquery to get the newest ticket date for each prospect
            newest_ticket_subquery = ProspectTicket.objects.filter(
                prospect_id=OuterRef('pk')
            ).order_by('-date').values('date', 'open')[:1]

            # Filter prospects by the newest ticket date within the time period
            stale_prospects = Prospect.objects.annotate(
                newest_ticket_date=Subquery(newest_ticket_subquery.values('date')[:1]),
                newest_ticket_open=Subquery(newest_ticket_subquery.values('open')[:1])
            ).filter(
                newest_ticket_date__date=reminder_date,
                newest_ticket_open=True
            )

            for prospect in stale_prospects:
                # Get the in_charge for the prospect
                in_charge_email = prospect.in_charge.email
                # print(in_charge_email)
                # print(settings.EMAIL_HOST_USER)

                # Send reminder email
                send_mail(
                    f'Reminder: Follow-Up dengan Prospect: {prospect.nama}',
                    f'Halo {prospect.in_charge.username},\n\nMohon follow-up dengan {prospect.nama}.\n\nSudah {period} hari setelah anda update ticketing di portal untuk {prospect.nama}. \n\n Klik link berikut untuk update ticketing: \nhttp://159.223.33.190/prospect_log/{prospect.prospect_id} \n\n\nTerima Kasih,\nLotus Sysdev',
                    settings.EMAIL_HOST_USER,
                    [in_charge_email],
                    fail_silently=False,
                )

                # Break the loop to send only one email per prospect
                break

        self.stdout.write(self.style.SUCCESS('Reminder emails sent successfully'))
