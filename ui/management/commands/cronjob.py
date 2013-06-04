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

class Command(NoArgsCommand):
    def handle_noargs(self, **_options):
        pass
        
