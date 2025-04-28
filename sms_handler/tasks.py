
from celery import shared_task
from .utils import process_message_with_ai, send_sms_response
@shared_task
def handle_incoming_sms(sender, message_text):
    # 1. Process the incoming message
    response_text = process_message_with_ai(message_text)

    # 2. Send back a response SMS
    send_sms_response(sender, response_text)