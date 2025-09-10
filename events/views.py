from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from events.services import EventService


def health_check(_request):
    """
    A simple view to check if the application is running.
    """
    return JsonResponse({"status": "ok", "message": "Application is running"})


@csrf_exempt
def webhook(request):
    return EventService().handle_webhook(request)
