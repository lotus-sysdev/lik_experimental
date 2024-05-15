from django.core.management import call_command

class MyCronJob():
    call_command("reminder")
