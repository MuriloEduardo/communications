from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from events.services import EventService


@csrf_exempt
def webhook(request):
    EventService().handle_webhook(request)

    return HttpResponse(status=200)
