from django.shortcuts import render
from places.models import Spot

# Create your views here.


def index(request):
    return render(request, "articles/index.html")


def search(request):
    if request.method == "GET":
        searched = request.GET.get("search")
        if searched:
            spots = Spot.objects.filter(title__contains=searched)
            print(spots)
            context = {
                "search": searched,
                "spots": spots,
            }
        else:
            context = {
                "search": searched,
            }
        return render(request, "articles/search.html", context)
    else:
        return render(request, "articles/index.html")
