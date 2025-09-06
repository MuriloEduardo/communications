import os
from events.integrations.base import MessagingIntegration


class WhatsAppService(MessagingIntegration):
    def __init__(
        self,
        graph_api_token=os.getenv("WHATSAPP_GRAPH_API_TOKEN"),
        webhook_verify_token=os.getenv("WHATSAPP_WEBHOOK_VERIFY_TOKEN"),
    ):
        self.graph_api_token = graph_api_token
        self.webhook_verify_token = webhook_verify_token
        print(f"Initialized WhatsAppService with Graph API Token: {graph_api_token}")

    def send_message(self, from_, to_number, message):
        msg = "Sending WhatsApp message from %s to %s: %s" % (from_, to_number, message)
        print(msg)

    def handle_webhook(self, request):
        return (
            request.POST.get("To"),
            request.POST.get("From"),
            request.POST.get("Body"),
        )
