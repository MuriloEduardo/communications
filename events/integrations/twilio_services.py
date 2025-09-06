import os

from twilio.rest import Client


class TwilioService:
    def __init__(
        self,
        auth_token=os.getenv("TWILIO_AUTH_TOKEN"),
        account_sid=os.getenv("TWILIO_ACCOUNT_SID"),
        from_number=os.getenv("TWILIO_FROM_NUMBER"),
    ):
        self.from_number = from_number
        self.client = Client(account_sid, auth_token)

    def send(self, from_, to_number, message):
        message = self.client.messages.create(
            body=message, from_=from_ or self.from_number, to=to_number
        )

        print("WhatsApp Message:", message)

        return message
