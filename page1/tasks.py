from .models import Prospect, ProspectLog
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings

def send_reminder_email():
    prospects = Prospect.objects.all()

    for prospect in prospects:
        last_activity = prospect.prospectlog_set.order_by('-date').first()

        if last_activity:
            days_since_last_activity = (timezone.now() - last_activity.date).days
        else:
            days_since_last_activity = (timezone.now() - prospect.tanggal).days
        
        if days_since_last_activity in [3,7,14,30]:
            subject = f"Reminder: Follow-Up dengan Prospect: {prospect.nama}"
            message = f"Hi {prospect.in_charge}, \n\nMohon follow-up dengan {prospect.nama}. \n\nJika sudah, jangan lupa untuk tambahkan kedalam prospect log di \nhttp://159.223.33.190/prospect_log/{prospect.prospect_id}"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [prospect.in_charge.email])V