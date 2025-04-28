import africastalking

from djangoProject import settings


def process_message_with_ai(message_text):
    # This is where you would implement your AI processing logic
    # For example, you might call an external AI API or use a local model

    # Simple example:
    if "hello" in message_text.lower():
        return "Hello! How can I assist you today?"
    elif "help" in message_text.lower():
        return "I can help you with various tasks. Just tell me what you need!"
    else:
        return "Thank you for your message. I'll process it and get back to you soon."


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
