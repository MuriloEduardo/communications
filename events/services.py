import os
from celery import Celery

from events.integrations.twilio_services import TwilioService
from events.integrations.whatsapp_services import WhatsAppService


class EventService:
    """Service that resolves messaging provider per-company and delegates.

    Provider resolution order:
    - request.POST['Provider'] (if present)
    - env var DEFAULT_MESSAGING_PROVIDER

    Supported providers: 'twilio', 'whatsapp'
    """

    def __init__(self):
        self._integration = None
        self.celery_client = Celery("maestro")

    def _get_provider_from_request(self, request):
        return request.POST.get("Provider")

    def _resolve_provider(self, request):
        provider = self._get_provider_from_request(request)
        if provider:
            return provider.lower()

        return os.getenv("DEFAULT_MESSAGING_PROVIDER", "twilio").lower()

    def _get_integration(self, provider):
        """Instantiate the correct integration for the provider."""
        if provider == "twilio":
            # TwilioService will validate env vars in its constructor
            return TwilioService()

        if provider == "whatsapp":
            # WhatsAppService doesn't require credentials here by default
            account_sid = os.getenv("WHATSAPP_ACCOUNT_SID")
            auth_token = os.getenv("WHATSAPP_AUTH_TOKEN")
            return WhatsAppService(
                account_sid=account_sid, auth_token=auth_token
            )

        raise ValueError(f"Unsupported messaging provider: {provider}")

    def handle_webhook(self, request):
        print(f"Processing event: {request}")
        to, from_, input_ = (
            request.POST.get("To"),
            request.POST.get("From"),
            request.POST.get("Body"),
        )

        result = self.celery_client.send_task(
            "executor.tasks.run",
            queue="toprocess",
            kwargs={
                "to": to,
                "from_": from_,
                "input": input_,
            },
        )

        print(f"Enviando mensagem via provider task: {result}")

    def send_message(self, to, from_, message, request=None):
        """Send a message using the provider resolved from request or env.

        If request is provided, provider resolution will prefer
        request.POST['Provider'].
        """
        provider = (
            self._resolve_provider(request)
            if request is not None
            else os.getenv("DEFAULT_MESSAGING_PROVIDER", "twilio")
        )

        print(
            "Sending message to %s from %s with content: %s using provider %s"
            % (to, from_, message, provider)
        )

        integration = self._get_integration(provider)

        result = integration.send_message(
            from_=from_, to_number=to, message=message
        )

        print("Message sent via integration:", result)

        return result
