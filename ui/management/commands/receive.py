import re
import sys
import email
import smtplib
import datetime

from django.utils import timezone
from django.core.management.base import NoArgsCommand
from django.conf import settings

from ui.models import Email

def reply(message, text):
    smtp = smtplib.SMTP('localhost')
    smtp.sendmail(message['to'], message['from'], text)
    smtp.quit()
    
def extract_email(addr):
    return email.utils.parseaddr(addr)[1]

def parse_timestamp(ts_text):
    """ Returns datetime object from a string, or raises ValueError """
    ts_text = re.sub(r'[^0-9]+', '', ts_text)
    ts_text += (12 - len(ts_text)) * '0'
    
    TS_FORMAT = '%Y%m%d%H%M'
    return datetime.datetime.strptime(ts_text, TS_FORMAT)

def process_message(message):
    server_address = extract_email(message['to'])
    client_address = extract_email(message['from'])
    
    match = re.match(settings.PINGME_CATCH_REGEX, server_address)
    if not match:
        reply(message, 'Unrecognized target address: %s' % server_address)
        
    
    timestamp = timezone.make_aware(parse_datetime(match.group(1)), timezone.get_current_timezone())
    
    return_message = email.message.Message()
    return_message['to'] = client_address
    return_message['from'] = server_address
    return_message['subject'] = message['subject']
    return_message.set_payload(message.get_payload()) 
    
    dbe = Email.objects.create(
        return_date=timestamp,
        client_address=client_address,
        server_address=server_address,
        mime_payload=return_message.as_string()
    )
        
    reply(message, 'Successfully enqueued for delivery on %s with id %s.' % (timestamp, dbe.id))

class Command(NoArgsCommand):
    def handle_noargs(self, **_options):
        message = email.message_from_file(sys.stdin)
        process_message(message)
