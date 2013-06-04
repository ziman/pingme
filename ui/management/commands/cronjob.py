from django.utils import timezone
from django.core.management.base import NoArgsCommand

from ui.models import Email

class Command(NoArgsCommand):
    def handle_noargs(self, **_options):
        now = timezone.now()
        for email in Email.objects.filter(return_date__lte=now):
            email.send()
            email.delete()        
