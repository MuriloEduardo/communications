from django.http import JsonResponse


def health_check(_request):
    """
    A simple view to check if the application is running.
    """
    return JsonResponse({"status": "ok", "message": "Application is running"})
