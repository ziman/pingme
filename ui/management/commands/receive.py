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
    
def extract_email(addr):
    return email.utils.parseaddr(addr)[1]

def process_message(message):
    server_address = extract_email(message['to'])
    client_address = extract_email(message['from'])
    
    match = re.match(r'^pingme-([^@]+)@functor.sk$', server_address)
    if not match:
        reply(message, 'Unrecognized target address: %s' % server_address)
        
    ts_text = re.sub(r'[^0-9]+', '', match.group(1))
    ts_text += (12 - len(ts_text)) * '0'
    
    TS_FORMAT = '%Y%m%d%H%M' 
    timestamp = timezone.make_aware(datetime.datetime.strptime(ts_text, TS_FORMAT), timezone.get_current_timezone())
    
    return_message = email.message.Message()
    return_message['to'] = client_address
    return_message['from'] = server_address
    return_message['subject'] = message['subject']
    return_message.set_payload(message.get_payload()) 
    
    email = Email.objects.create(
        return_date=timestamp,
        client_address=client_address,
        server_address=server_address,
        mime_payload=return_message.as_string()
    )
        
    reply(message, 'Successfully enqueued for delivery on %s with id %s.' % (timestamp, email.id))

class Command(NoArgsCommand):
    def handle_noargs(self, **_options):
        message = email.message_from_file(sys.stdin)
        process_message(message)
