import os

import africastalking
import requests
from together import Together
from django.conf import settings

from djangoProject import settings



def process_message_with_ai(message_text):
    """
    Process an incoming SMS message for Ugandan primary students using Together.ai (Llama 3.1 8B).
    """
    client = Together(api_key=settings.TOGETHER_API_KEY)

    system_instruction = (
        "You are an educational assistant helping primary school students in Uganda. "
        "Answer questions clearly, politely, and briefly. "
        "Keep all answers under 100 characters. Use simple English."
    )

    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": message_text}
        ]
    )

    return response.choices[0].message.content.strip()

def send_sms_response(recipient, message):
    # Implementation for sending SMS response using Africa's Talking API
    username = settings.AFRICAS_TALKING_USERNAME
    api_key = settings.AFRICAS_TALKING_API_KEY
    sender = settings.AFRICAS_TALKING_SMS_SHORTCODE

    africastalking.initialize(
        username=username,
        api_key=api_key
    )

    sms = africastalking.SMS
    try:
        response = sms.send(message, [recipient], sender)
        print(response)
    except Exception as e:
        print(f'Arthur, we have a problem: {e}')
