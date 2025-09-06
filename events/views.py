from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from events.services import EventService


@csrf_exempt
def webhook(request):
    if request.method == "POST" or request.method == "GET":
        EventService().handle_webhook(request)
    else:
        return HttpResponse(status=405)  # Method Not Allowed
    return HttpResponse(status=200)
