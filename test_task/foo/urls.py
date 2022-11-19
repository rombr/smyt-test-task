from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path(
        "api/<str:model_name>/<int:object_id>/",
        views.api_details,
        name="api_details",
    ),
    path("api/<str:model_name>/", views.api, name="api"),
]
