import re
import sys
import email
import smtplib
import datetime

from django.utils import timezone
from django.core.management.base import NoArgsCommand

from ui.models import Email

def reply(message, text):
    smtp = smtplib.SMTP('localhost')
    smtp.sendmail(message['to'], message['from'], text)
    smtp.quit()

def process_message(message):
    match = re.match(r'^pingme-([^@]+)@functor.sk$', message['to'])
    if not match:
        reply(message, 'Unrecognized target address: %s' % message['to'])
        
    ts_text = re.sub(r'[^0-9]+', '', match.group(1))
    ts_text += (12 - len(ts_text)) * '0'
    
    TS_FORMAT = '%Y%m%d%H%M' 
    timestamp = timezone.make_aware(datetime.datetime.strptime(ts_text, TS_FORMAT), timezone.get_current_timezone())
    
    email = Email.objects.create(
        return_date=timestamp,
        client_address=message['from'],
        server_address=message['to'],
        mime_payload=message.as_string()
    )
        
    reply(message, 'Successfully enqueued for delivery on %s with id %s.' % (timestamp, email.id))

class Command(NoArgsCommand):
    def handle_noargs(self, **_options):
        message = email.message_from_file(sys.stdin)
        process_message(message)
