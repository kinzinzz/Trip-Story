from django.shortcuts import render, redirect, get_object_or_404
from . import models
from . import forms
from django.http import JsonResponse
from django.db.models import Count
from .models import Review
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.core.paginator import Paginator

# 리뷰 인덱스
def index(request):
    # 페이징 처리
    # like 많은순으로 정렬하고 0~2등 가져오기
    reviews = (
        models.Review.objects.all()
        .annotate(like_count=Count("like"))
        .order_by("-like_count")[0:6]
    )

    return render(request, "reviews/index.html", {"reviews": reviews})


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
    if request.user != review.user1:
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
    if request.user != review.user1:
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

    return redirect("reviews:detail", review_pk)


# 좋아요 기능 비동기
# if request.user in review.like.all():
#     review.like.remove(request.user)
#     # request.user가 이전에 좋아요를 클릭한 사람이라면 좋아요 취소
#     existed_user = False

# else:
#     review.like.add(request.user)
#     # request.user가 이전에 좋아요를 클릭한 사람이 아니라면 좋아요
#     existed_user = True
# likeCount = review.like.count()
# context = {
#     "existed_user": existed_user,
#     "likeCount": likeCount,
# }

# return JsonResponse(context)
