from django.urls import path
from . import views

app_name = "places"

urlpatterns = [
    path("inform/", views.inform, name="inform"),
    path("<cityname>", views.city, name="city"),
    path("citycreate/", views.citycreate, name="citycreate"),
    path("<cityname>/allspots", views.allspots, name="allspots"),
    path("<cityname>/<int:pk>/", views.spot, name="spot"),
    path("<cityname>/createspot", views.createspot, name="createspot"),
    path("<cityname>/<int:pk>/comments", views.spotcomment, name="spotcomment"),
    path(
        "<cityname>/<int:pk>/comments/delete/<int:comment_pk>",
        views.comment_delete,
        name="comment_delete",
    ),
]
