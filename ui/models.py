from django.db import models

class Email(models.Model):
    address = models.EmailField()
    return_date = models.DateTimeField()
    mime_payload = models.TextField()
