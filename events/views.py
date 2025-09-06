from django.views.decorators.csrf import csrf_exempt

from events.services import EventService


@csrf_exempt
def webhook(request):
    return EventService().handle_webhook(request)
