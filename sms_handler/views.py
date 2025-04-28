# views.py
import africastalking
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
import requests
from .models import SMSMessage  # We'll create this model next
from .tasks import handle_incoming_sms


@csrf_exempt  # Required since Africa's Talking will post from external source
def sms_callback(request):
    if request.method == 'POST':
        # Extract data from the POST request
        sender = request.POST.get('from', '')
        to = request.POST.get('to', '')
        text = request.POST.get('text', '')
        date = request.POST.get('date', '')
        id = request.POST.get('id', '')
        linkId = request.POST.get('linkId', '')

        # Save the message to the database
        message = SMSMessage.objects.create(
            sender=sender,
            recipient=to,
            message_text=text,
            message_date=date,
            message_id=id,
            link_id=linkId
        )


        # 👉 Queue the task
        handle_incoming_sms.delay(sender, text)

        # Return a 200 OK response to Africa's Talking immediately
        return HttpResponse("OK", status=200)
    return HttpResponse("Method not allowed", status=405)

