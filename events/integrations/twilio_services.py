import os
from twilio.rest import Client
from events.integrations.base import MessagingIntegration


class TwilioService(MessagingIntegration):
    def __init__(
        self,
        auth_token=os.getenv("TWILIO_AUTH_TOKEN"),
        account_sid=os.getenv("TWILIO_ACCOUNT_SID"),
        from_number=os.getenv("TWILIO_FROM_NUMBER"),
    ):
        self.from_number = from_number

        if not account_sid or not auth_token:
            raise ValueError("Twilio credentials not configured")

        self.client = Client(account_sid, auth_token)

    def send_message(self, from_, to_number, message):
        message = self.client.messages.create(
            body=message, from_=from_ or self.from_number, to=to_number
        )

        return message

    def get_props(self, request):
        return (
            request.POST.get("To"),
            request.POST.get("From"),
            request.POST.get("Body"),
        )

    def verify_webhook_token(self, request):
        # Twilio does not require token verification for webhooks
        pass
