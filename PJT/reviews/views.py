from django.shortcuts import render, redirect, get_object_or_404
from . import models
from . import forms
from django.http import JsonResponse
from django.db.models import Count

# 리뷰 인덱스
def index(request):
    # like 많은순으로 정렬하고 0~2등 가져오기
    reviews = (
        models.Review.objects.all()
        .annotate(like_count=Count("like"))
        .order_by("-like_count")[0:3]
    )

    print(reviews)
    return render(request, "reviews/index.html", {"reviews": reviews})


# 리뷰 생성
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
def update(request, review_pk):
    review = get_object_or_404(models.Review, pk=review_pk)

    if request.method == "POST":
        form = forms.ReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            form.save()
            return redirect("reviews:detail", review_pk)

    else:
        form = forms.ReviewForm(instance=review)

    return render(request, "reviews/update.html", {"form": form})


# 리뷰 삭제
def delete(request, review_pk):
    review = get_object_or_404(models.Review, pk=review_pk)

    review.delete()

    return redirect("reviews:index")


#  리뷰 좋아요
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
