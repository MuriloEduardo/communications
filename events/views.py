from django.http import HttpResponse


def webhook(request):
    print("Webhook received", request)
    return HttpResponse("Hello world!")
