from celery import shared_task

from events.integrations.twilio_services import TwilioService

twilio_service = TwilioService()


@shared_task(queue="ai-postprocessing")
def postprocessing(*args, **kwargs):
    print("Postprocessing task executed with args:", args, "and kwargs:", kwargs)

    result = twilio_service.send(
        to_number="whatsapp:+555174019092",
        message="Postprocessing task completed successfully.",
    )

    print("WhatsApp Message sent:", result)
