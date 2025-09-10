from django.urls import path
from . import views

urlpatterns = [
    path("webhook/", views.webhook, name="webhook"),
    path("health_check/", views.health_check, name="health_check"),
]
