import re
import sys
import email
import smtplib

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
        reply(message, 'Unrecognized target address: %s' % match.group(1))
        
    reply(message, 'Recognized target address: %s' % match.group(1))

class Command(NoArgsCommand):
    def handle_noargs(self, **_options):
        message = email.message_from_file(sys.stdin)
        process_message(message)
