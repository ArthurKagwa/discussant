import datetime
import os

import africastalking
import requests
from django.db.models import Q
from together import Together
from django.conf import settings

from djangoProject import settings
from .models import SMSMessage



def process_message_with_ai(message_text, sender):

    client = Together(api_key=settings.TOGETHER_API_KEY)

    system_instruction = (
        """You are a friendly and knowledgeable educational assistant helping primary school students in Uganda. 
You tutor science, social studies, mathematics, and English. 
Use clear, simple, and polite language appropriate for children aged 8 to 14. 
Be brief but conversational—responses should be helpful and no longer than 300 characters.

Always base your answers on accurate, scientific facts aligned with the Ugandan NCDC curriculum and UNEB standards. 
You may ask a simple follow-up question if it helps the student learn better.

If you don't know the answer, say: "I don't know."  
If the question is unrelated to school subjects, say: "I can't help with that."  
If a question is in a local language, reply in the same local language.

Avoid unnecessary explanations or opinions. Keep responses focused, helpful, and child-friendly."""

    )
    # get sms history from database
    sms_history = get_sms_history(sender)



    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3",
        messages=[
            {"role": "system", "content": system_instruction},
            *sms_history,  # Add past messages
            {"role": "user", "content": message_text}  # Current message
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
    date= datetime.date.today()

    sms = africastalking.SMS
    try:
        response = sms.send(message, [recipient], sender)
        message = SMSMessage.objects.create(
            sender="system",
            recipient=sender,
            message_text=message,
            message_date=date,
            message_id=id
        )
        print(response)
    except Exception as e:
        print(f'Arthur, we have a problem: {e}')

def get_sms_history(sender):
    """
    Get the last 6 message exchanges between a student and the system (AI).
    """
    # Filter messages where the sender or recipient is the student
    messages = SMSMessage.objects.filter(Q(sender=sender) | Q(recipient=sender)).order_by('-created_at')[:6]
    # Reverse to chronological order
    messages = reversed(messages)

    # Convert to chat format
    chat_messages = []
    for msg in messages:
        if msg.sender == "system":
            role = "assistant"
        elif msg.sender == sender:
            role = "user"
        else:
            continue  # ignore unexpected data

        chat_messages.append({"role": role, "content": msg.message_text})

    return chat_messages
