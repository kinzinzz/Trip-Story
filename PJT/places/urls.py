from django.urls import path
from . import views

app_name = "places"

urlpatterns = [
    path("inform/", views.inform, name="inform"),
    path("<cityname>", views.city, name="city"),
    path("citycreate/", views.citycreate, name="citycreate"),
    path("place/", views.place, name="place"),
]
