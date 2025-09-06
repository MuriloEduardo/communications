from celery import shared_task

from events.integrations.twilio_services import TwilioService

twilio_service = TwilioService()


@shared_task(queue="ai-postprocessing")
def postprocessing(*args, **kwargs):
    print(
        "Postprocessing task executed with args:",
        args,
        "and kwargs:",
        kwargs,
    )

    result = twilio_service.send(
        from_=f"whatsapp:{kwargs.get('from_')}",
        to_number=f"whatsapp:{kwargs.get('to')}",
        message=kwargs.get("message", "Hello from Twilio via WhatsApp!"),
    )

    print("WhatsApp Message sent:", result)
