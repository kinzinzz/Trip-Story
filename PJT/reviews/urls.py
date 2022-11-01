from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path('review/', views.review, name='review'),
    path('review_create/', views.review_create, name='review_create'),
]
