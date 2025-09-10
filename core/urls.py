from . import views
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("/", views.health_check, name="health_check"),
    path("admin/", admin.site.urls),
    path("events/", include("events.urls")),
]
