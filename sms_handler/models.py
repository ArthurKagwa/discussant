# models.py
from django.db import models


class SMSMessage(models.Model):
    sender = models.CharField(max_length=20)
    recipient = models.CharField(max_length=20)
    message_text = models.TextField()
    message_date = models.CharField(max_length=50)  # We'll store the date as received from Africa's Talking
    message_id = models.CharField(max_length=50)
    link_id = models.CharField(max_length=100, blank=True, null=True)
    processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} on {self.message_date}"