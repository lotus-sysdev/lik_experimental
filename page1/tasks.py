from celery import shared_task
from django.core.management import call_command

@shared_task
def run_reminder():
    call_command('reminder')