class WhatsAppService:
    def __init__(self, account_sid, auth_token):
        self.account_sid = account_sid
        self.auth_token = auth_token
        print(f"Initialized WhatsAppService with SID: {account_sid}")

    def send_message(self, from_, to_number, message):
        print(f"Sending WhatsApp message from {from_} to {to_number}: {message}")

    def handle_webhook(self, message):
        print("Handling WhatsApp webhook:", message)
