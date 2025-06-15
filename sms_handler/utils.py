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
        """You are a knowledgeable educational assistant helping primary school students in Uganda. 
You tutor science, social studies, mathematics, and English. 
Give brief but conversational—responses should be helpful and no longer than 300 characters.
Always base your answers on accurate, scientific facts.
If you don't know the answer, say: "I don't know."  
If the question is unrelated to school subjects, say: "I can't help with that." 
If a question is in a local language, reply in the same local language.
If you’ve asked a question and receive affirmation immediately  answer don’t re-greet or switch topics.
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
        ],
        temperature=0.5,
        max_tokens=150,
        top_p=0.9,
        frequency_penalty=0.2,
        presence_penalty=0.1,
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
            sender="assistant",
            recipient=sender,
            message_text=message,
            message_date=date,
            message_id=id
        )
        print(response)
    except Exception as e:
        print(f'Arthur, we have a problem: {e}')

def get_sms_history(sender, limit=6):
    """
    Retrieve the last `limit` exchanges between a student and the AI,
    in proper chronological order and chat-API format.
    """
    # 1. Fetch most recent messages involving this sender
    recent = (SMSMessage.objects
                     .filter(Q(sender=sender) | Q(recipient=sender))
                     .order_by('-created_at')[:limit])

    # 2. Reverse into chronological order
    recent = list(recent)[::-1]

    # 3. Map to chat roles
    chat = []
    for msg in recent:
        text = msg.message_text.strip()
        # Normalize system/AI tags
        if msg.sender.lower() in {"system", "assistant", "ai"}:
            role = "assistant"
        elif msg.sender == sender:
            role = "user"
        else:
            continue

        chat.append({"role": role, "content": text})
    return chat
