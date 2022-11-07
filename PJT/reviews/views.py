from django.shortcuts import render, redirect, get_object_or_404
from . import models
from . import forms
from django.http import JsonResponse
from django.db.models import Count
from .models import Review
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from places.models import City
from django.contrib import messages

from django.db.models import Q
from places.models import City


# 리뷰 인덱스
def index(request):
    # 페이징 처리
    # like 많은순으로 정렬하고 0~2등 가져오기
    citys = City.objects.all()
    page = request.GET.get("page", "1")
    page_li = Review.objects.all()
    pag = page_li.annotate(like_count=Count("like"))
    page_ = pag.order_by("-pk")  # 작성 순으로 바꿨습니다.
    paginator = Paginator(page_, 6)
    page_obj = paginator.get_page(page)

    context = {"pageboard": page_obj, "citys": citys}

    return render(request, "reviews/index.html", context)


# 리뷰 생성
@login_required(login_url="accounts:login")
def create(request):

    if request.method == "POST":
        form = forms.ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()

            return redirect("reviews:index")

    else:
        form = forms.ReviewForm()

    return render(request, "reviews/create.html", {"form": form})


# 리뷰 상세페이지
def detail(request, review_pk):

    review = get_object_or_404(models.Review, pk=review_pk)

    return render(request, "reviews/detail.html", {"review": review})


# 리뷰 수정
@login_required(login_url="accounts:login")
def update(request, review_pk):
    review = get_object_or_404(models.Review, pk=review_pk)
    # 리뷰 작성자가 아니면 수정 권한 없음
    if request.user != review.user:
        messages.error(request, "권한이 없습니다.")
        return redirect("reviews:detail", review_pk)

    if request.method == "POST":
        form = forms.ReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            form.save()
            return redirect("reviews:detail", review_pk)

    else:
        form = forms.ReviewForm(instance=review)

    return render(request, "reviews/update.html", {"form": form})


# 리뷰 삭제
@login_required(login_url="accounts:login")
def delete(request, review_pk):
    review = get_object_or_404(models.Review, pk=review_pk)
    # 리뷰 작성자가 아니면 삭제 권한 없음
    if request.user != review.user:
        messages.error(request, "권한이 없습니다.")
        return redirect("reviews:detail", review_pk)
    review.delete()

    return redirect("reviews:index")


#  리뷰 좋아요
@login_required(login_url="accounts:login")
def like(request, review_pk):

    review = get_object_or_404(models.Review, pk=review_pk)

    if request.user in review.like.all():
        review.like.remove(request.user)
    else:
        review.like.add(request.user)

    return redirect("reviews:index")


# 리뷰 도시별 조회
def search_reviews(request, city_name):
    citys = City.objects.all()
    query = City.objects.get(name=city_name).id
    reviews = (
        models.Review.objects.all().filter(Q(city__exact=query)).order_by("-created_at")
    )

    return render(
        request,
        "reviews/search.html",
        {"reviews": reviews, "city_name": city_name, "citys": citys},
    )
