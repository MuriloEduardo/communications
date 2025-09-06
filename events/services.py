import os
from celery import Celery
from django.http import HttpResponse

from events.integrations.twilio_services import TwilioService
from events.integrations.whatsapp_services import WhatsAppService


class EventService:
    """
    Service that resolves messaging provider per-company and delegates.
    """

    def __init__(self):
        self.celery_client = Celery("maestro")
        self.provider = os.getenv("DEFAULT_MESSAGING_PROVIDER", "whatsapp")

        if self.provider == "twilio":
            self._integration = TwilioService()

        if self.provider == "whatsapp":
            self._integration = WhatsAppService()

    def handle_webhook(self, request):
        """
        Process incoming webhook and delegate to Celery task.
        """
        if request.method == "GET":
            return self._integration.verify_webhook_token(request)
        else:
            to, from_, input_ = self._integration.get_props(request)

            result = self.celery_client.send_task(
                "executor.tasks.run",
                queue="toprocess",
                kwargs={
                    "to": to,
                    "from_": from_,
                    "input": input_,
                },
            )

            print("Task dispatched to Celery:", result)

            return HttpResponse(status=200)

    def send_message(self, to, from_, message):
        """
        Send a message using the provider resolved from request or env.
        """
        result = self._integration.send_message(
            from_=from_, to_number=to, message=message
        )

        print("Message sent via integration:", result)

        return result
