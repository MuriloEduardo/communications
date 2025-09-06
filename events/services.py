from celery import Celery

from events.integrations.twilio_services import TwilioService


class EventService:
    def __init__(self):
        self.twilio_service = TwilioService()
        self.celery_client = Celery("maestro")

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

        print(f"Enviando mensagem via WhatsApp: {result}")

    def send_message(self, to, from_, message):
        print(f"Sending message to {to} from {from_} with content: {message}")

        result = self.twilio_service.send_message(
            from_=from_,
            to_number=to,
            message=message,
        )

        print("WhatsApp Message sent:", result)

        return result
