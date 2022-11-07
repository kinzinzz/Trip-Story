from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("community/", views.community, name="community"),
    path("community/create", views.com_create, name="com_create"),
    path("community/<int:pk>", views.com_detail, name="com_detail"),
    path("community/<int:pk>/comments/", views.com_comment, name="com_comment"),
    path(
        "community/<int:pk>/comments/<int:comment_pk>/",
        views.co_delete,
        name="co_delete",
    ),
    path("community/<int:pk>/update", views.com_update, name="com_update"),
    path("community/<int:pk>/delete", views.com_delete, name="com_delete"),
]
