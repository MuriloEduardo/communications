from events.integrations.base import MessagingIntegration


class WhatsAppService(MessagingIntegration):
    def __init__(self, account_sid=None, auth_token=None):
        self.account_sid = account_sid
        self.auth_token = auth_token
        print(f"Initialized WhatsAppService with SID: {account_sid}")

    def send_message(self, from_, to_number, message):
        msg = "Sending WhatsApp message from %s to %s: %s" % (
            from_, to_number, message
        )
        print(msg)

    def handle_webhook(self, message):
        print("Handling WhatsApp webhook:", message)
