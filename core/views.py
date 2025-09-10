from django.http import JsonResponse


def home(request):
    """View simples para testar se a aplicação está funcionando."""
    return JsonResponse({
        "status": "ok",
        "message": "Maestro Communications API está funcionando!",
        "endpoints": {
            "webhook": "/events/webhook/",
            "admin": "/admin/"
        }
    })


def health_check(request):
    """Health check endpoint para monitoramento."""
    return JsonResponse({"status": "healthy"})
