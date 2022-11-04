from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    # 리뷰 인덱스
    path("", views.index, name="index"),
    # 리뷰 생성
    path("create/", views.create, name="create"),
    # 리뷰 상세
    path("<int:review_pk>/", views.detail, name="detail"),
    # 리뷰 수정
    path("<int:review_pk>/update/", views.update, name="update"),
    # 리뷰 삭제
    path("<int:review_pk>/delete/", views.delete, name="delete"),
    # 리뷰 좋아요
    path("<int:review_pk>/like/", views.like, name="like"),
    # 도시별 리뷰 조회
    path("search/", views.search, name="search"),
]
