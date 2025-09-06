from django.views.decorators.csrf import csrf_exempt

from events.services import EventService


@csrf_exempt
def webhook(request):
    response = EventService().handle_webhook(request)
    return response
