from django.shortcuts import render, redirect
from places.models import Spot
from reviews.models import Review
from .models import Community, Comcomment
from .forms import CommunityForm, ComcommentForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.paginator import Paginator

# Create your views here.


def index(request):
    reviews = Review.objects.annotate(like_count=Count("like")).order_by("-like_count")[
        :3
    ]
    context = {
        "reviews": reviews,
    }
    return render(request, "articles/index.html", context)


def search(request):
    if request.method == "GET":
        searched = request.GET.get("search")
        if searched:
            spots = Spot.objects.filter(title__contains=searched)
            reviews = Review.objects.filter(title__contains=searched)
            for review in reviews:
                print(review.title)
            context = {
                "search": searched,
                "spots": spots,
                "reviews": reviews,
            }
        else:
            context = {
                "search": searched,
            }
        return render(request, "articles/search.html", context)
    else:
        return render(request, "articles/index.html")


def community(request):
    page = request.GET.get("page", "1")
    pag = Community.objects.order_by("-pk")
    paginator = Paginator(pag, 10)
    page_obj = paginator.get_page(page)
    context = {
        "coms": page_obj,
    }
    return render(request, "articles/community.html", context)


@login_required
def com_create(request):
    if request.method == "POST":
        com_form = CommunityForm(request.POST)
        if com_form.is_valid():
            com = com_form.save(commit=False)
            com.user = request.user
            com.save()
            return redirect("articles:community")
    else:
        com_form = CommunityForm()
    context = {
        "com_form": com_form,
    }
    return render(request, "articles/com_form.html", context)


@login_required
def com_detail(request, pk):
    com = Community.objects.get(pk=pk)
    comment_form = ComcommentForm()
    comments = com.comcomment_set.all()
    context = {
        "com": com,
        "comment_form": comment_form,
        "comments": comments,
    }
    return render(request, "articles/com_detail.html", context)


@login_required
def com_comment(request, pk):
    com = Community.objects.get(pk=pk)
    comment_form = ComcommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.community = com
        comment.user = request.user
        comment.save()
    return redirect("articles:com_detail", pk)


def co_delete(request, com_pk, comment_pk):
    Comcomment.objects.get(pk=comment_pk).delete()
    return redirect("articles:com_detail", com_pk)


def com_update(request, pk):
    com = Community.objects.get(pk=pk)
    if request.method == "POST":
        com_form = CommunityForm(request.POST, instance=com)
        if com_form.is_valid():
            com.save()
            return redirect("articles:com_detail", pk)
    else:
        com_form = CommunityForm(instance=com)
    context = {
        "com_form": com_form,
    }
    return render(request, "articles/com_form.html", context)


def com_delete(request, pk):
    Community.objects.get(pk=pk).delete()
    return redirect("articles:community")
