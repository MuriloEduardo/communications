import os
import json
import requests
from django.http import HttpResponse
from typing import Any, Dict, Optional
from events.integrations.base import MessagingIntegration


class WhatsAppService(MessagingIntegration):
    def __init__(
        self,
        graph_api_token: Optional[str] = os.getenv("WHATSAPP_GRAPH_API_TOKEN"),
        webhook_verify_token: Optional[str] = os.getenv(
            "WHATSAPP_WEBHOOK_VERIFY_TOKEN"
        ),
        phone_number_id: Optional[str] = os.getenv("WHATSAPP_PHONE_NUMBER_ID"),
        graph_api_version: str = os.getenv("WHATSAPP_GRAPH_API_VERSION", "v22.0"),
    ):
        self.graph_api_token = graph_api_token
        self.webhook_verify_token = webhook_verify_token
        self.phone_number_id = phone_number_id
        self.graph_api_version = graph_api_version

        print(
            "Initialized WhatsAppService with Graph API Token: %s" % (graph_api_token,)
        )

    def send_message(
        self,
        from_: Optional[str],
        to_number: str,
        message: Any = None,
        message_type: str = "template",
        template_name: Optional[str] = None,
        language_code: str = "en_US",
        components: Optional[Dict] = None,
        timeout: int = 10,
    ) -> Dict:
        """Send a message via Facebook Graph API (WhatsApp).

        Parameters are dynamic and will fall back to environment variables.

        - from_: phone_number_id to use in URL. If not provided, uses
          WHATSAPP_PHONE_NUMBER_ID env var.
        - to_number: recipient phone number (in international format without +)
        - message: for text messages this is the body string; for template
          messages this may be None (template_name used).
                - message_type: 'template' or 'text' or 'custom' (
                    if passing a full dict)
        - template_name / language_code: used when message_type == 'template'
        - components: optional dict to include template components
        """

        if not self.graph_api_token:
            raise ValueError("WHATSAPP_GRAPH_API_TOKEN is not configured")

        phone_id = from_ or self.phone_number_id
        if not phone_id:
            raise ValueError("WhatsApp phone number id not configured")

        url = (
            f"https://graph.facebook.com/{self.graph_api_version}"
            f"/{phone_id}/messages"
        )

        headers = {
            "Authorization": f"Bearer {self.graph_api_token}",
            "Content-Type": "application/json",
        }

        if message_type == "template":
            if not template_name:
                raise ValueError("template_name is required for template messages")

            payload: Dict[str, Any] = {
                "messaging_product": "whatsapp",
                "to": to_number,
                "type": "template",
                "template": {
                    "name": template_name,
                    "language": {"code": language_code},
                },
            }

            if components:
                payload["template"]["components"] = components

        elif message_type == "text":
            payload = {
                "messaging_product": "whatsapp",
                "to": to_number,
                "type": "text",
                "text": {"body": str(message)},
            }

        elif message_type == "custom" and isinstance(message, dict):
            payload = message

        else:
            raise ValueError("Unsupported message_type or invalid message payload")

        print("WhatsApp API request url:", url)
        print("WhatsApp API payload:", json.dumps(payload))

        resp = requests.post(url, headers=headers, json=payload, timeout=timeout)

        try:
            resp_json = resp.json()
        except ValueError:
            resp_json = {"status_code": resp.status_code, "text": resp.text}

        print("WhatsApp API response status:", resp.status_code)
        print("WhatsApp API response body:", resp_json)

        resp.raise_for_status()

        return resp_json

    def verify_webhook_token(self, request):
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")

        if mode == "subscribe" and token == self.webhook_verify_token:
            return HttpResponse(challenge, status=200)
        else:
            return HttpResponse("Verification token mismatch", status=403)

    def get_props(self, request):
        data = json.loads(request.body)

        from_ = data["entry"][0]["changes"][0]["value"]["messages"][0]["from"]
        to = data["entry"][0]["changes"][0]["value"]["metadata"]["display_phone_number"]
        body = (
            data["entry"][0]["changes"][0]["value"]["messages"][0]
            .get("text", {})
            .get("body", "")
        )

        return (
            to,
            from_,
            body,
        )
