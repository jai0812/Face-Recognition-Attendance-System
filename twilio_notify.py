# twilio_notify.py
import os
from twilio.rest import Client

# These should be set in your environment for security
SID          = os.getenv("TWILIO_ACCOUNT_SID")
TOKEN        = os.getenv("TWILIO_AUTH_TOKEN")
SMS_FROM     = os.getenv("TWILIO_PHONE_NUMBER")        # e.g. "+12025551212"
WA_FROM      = os.getenv("TWILIO_WHATSAPP_NUMBER")     # e.g. "whatsapp:+14155238886"

client = Client(SID, TOKEN)

def send_sms(to: str, body: str):
    """Send an SMS."""
    client.messages.create(
        body=body,
        from_=SMS_FROM,
        to=to
    )

def send_whatsapp(to: str, body: str):
    """Send a WhatsApp message via Twilio sandbox."""
    client.messages.create(
        body=body,
        from_=WA_FROM,
        to=f"whatsapp:{to}"
    )
