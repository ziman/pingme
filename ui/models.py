import email
import smtplib

from django.db import models

class Email(models.Model):
    client_address = models.EmailField()
    server_address = models.EmailField()
    return_date = models.DateTimeField()
    mime_payload = models.TextField()
    
    def send(self):
        smtp = smtplib.SMTP('localhost')
        smtp.sendmail(self.server_address, [self.client_address], self.mime_payload)
        smtp.quit()
    
    def __str__(self):
        return '%s: %s' % (self.return_date, self.client_address)
