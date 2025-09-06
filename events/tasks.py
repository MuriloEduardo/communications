from celery import shared_task

from events.services import EventService

event_service = EventService()


@shared_task(queue="ai-postprocessing")
def postprocessing(*args, **kwargs):
    print(
        "Postprocessing task executed with args:",
        args,
        "and kwargs:",
        kwargs,
    )

    result = event_service.send_message(
        to=kwargs.get("to"),
        from_=kwargs.get("from_"),
        message=kwargs.get("message", ""),
    )

    print("WhatsApp Message sent:", result)

    return result
