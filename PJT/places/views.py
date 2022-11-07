from django.shortcuts import render, redirect
from .models import City, Spot, Spotcomment
from .forms import CityForm, SpotForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count

# 날씨모듈
import requests
from bs4 import BeautifulSoup
from datetime import date


def inform(request):
    citys = City.objects.all()
    city3 = City.objects.order_by("-hits")[:3]
    context = {
        "citys": citys,
        "city3": city3,
    }
    return render(request, "places/inform.html", context)


def allspots(request, cityname):
    spots = Spot.objects.filter(city__name=cityname)
    context = {
        "spots": spots,
        "cityname": cityname,
    }
    return render(request, "places/allspots.html", context)


def city(request, cityname):
    city = City.objects.get(name=cityname)
    grades = (
        Spotcomment.objects.select_related("spot")
        .values("spot")
        .annotate(avg=Avg("grade"))
        .order_by("-avg")
        .filter(spot__city=city)
    )
    visiters = (
        Spotcomment.objects.select_related("spot")
        .values("spot")
        .annotate(cnt=Count("id"))
        .order_by("-cnt")
        .filter(spot__city=city)
    )
    visitspots = []
    for visiter in visiters:
        visitspots.append((Spot.objects.get(pk=visiter["spot"]), visiter["cnt"]))
        if len(visitspots) == 3:
            break
    spots = []
    for grade in grades:
        star = ""
        if grade["avg"]:
            if grade["avg"] > 4.9:
                star = "★★★★★"
            elif grade["avg"] > 4.4:
                star = "★★★★☆"
            elif grade["avg"] > 3.9:
                star = "★★★★"
            elif grade["avg"] > 3.4:
                star = "★★★☆"
            elif grade["avg"] > 2.9:
                star = "★★★"
            elif grade["avg"] > 2.4:
                star = "★★☆"
            elif grade["avg"] > 1.9:
                star = "★★"
            elif grade["avg"] > 1.4:
                star = "★☆"
            elif grade["avg"] > 0.9:
                star = "★"
            elif grade["avg"] > 0.4:
                star = "☆"
            else:
                star = "별점 없음"
        spots.append((Spot.objects.get(pk=grade["spot"]), star))
        if len(spots) == 3:
            break

    # 도시별 날씨예보

    today = date.today()
    time_list = ["현재날씨", "내일날씨", "모레날씨"]
    temp_data = {}

    for time in time_list:
        html = requests.get(
            f"https://search.naver.com/search.naver?query={city.name}{time}"
        )
        soup = BeautifulSoup(html.text, "html.parser")

        if time == "현재날씨":
            data = soup.find("div", {"class": "_today"})
            find_temp = data.find("div", {"class": "temperature_text"}).text.strip()[5:]
            find_sky = data.find("span", {"class": "weather before_slash"}).text.strip()
            temp_data[f"{time}"] = find_temp + " | " + find_sky

        else:
            html = requests.get(
                f"https://search.naver.com/search.naver?query={city.name}{time}"
            )
            am_data = soup.find("div", {"class": "_am"})
            find_am_temp = am_data.find(
                "div", {"class": "temperature_text"}
            ).text.strip()[5:]
            find_am_sky = am_data.find("p", {"class": "summary"}).text.strip()
            temp_data[f"am_{time}"] = find_am_temp + " | " + find_am_sky

            pm_data = soup.find("div", {"class": "_pm"})
            find_pm_temp = pm_data.find(
                "div", {"class": "temperature_text"}
            ).text.strip()[5:]
            find_pm_sky = pm_data.find("p", {"class": "summary"}).text.strip()
            temp_data[f"pm_{time}"] = find_pm_temp + " | " + find_pm_sky

    # 도시별 날씨 예보

    context = {
        "city": city,
        "spots": spots,
        "visitspots": visitspots,
        # 날씨 데이터
        "월": today.month,
        "일": today.day,
        "temp_data": temp_data,
    }

    return render(request, "places/city.html", context)


@login_required
def citycreate(request):
    if request.method == "POST":
        city_form = CityForm(request.POST, request.FILES)
        if city_form.is_valid():
            city_form.save()
            return redirect("places:inform")

    else:
        city_form = CityForm()

    context = {
        "city_form": city_form,
    }

    return render(request, "places/citycreate.html", context)


def spot(request, cityname, pk):
    spot = Spot.objects.get(pk=pk)
    comments = Spotcomment.objects.filter(spot=spot)
    comment_form = CommentForm()
    grade = comments.aggregate(avg=Avg("grade"))
    avg = "리뷰 없음"
    star = ""
    if grade["avg"]:
        if grade["avg"] > 4.9:
            star = "★★★★★"
        elif grade["avg"] > 4.4:
            star = "★★★★☆"
        elif grade["avg"] > 3.9:
            star = "★★★★"
        elif grade["avg"] > 3.4:
            star = "★★★☆"
        elif grade["avg"] > 2.9:
            star = "★★★"
        elif grade["avg"] > 2.4:
            star = "★★☆"
        elif grade["avg"] > 1.9:
            star = "★★"
        elif grade["avg"] > 1.4:
            star = "★☆"
        elif grade["avg"] > 0.9:
            star = "★"
        elif grade["avg"] > 0.4:
            star = "☆"
        else:
            avg = ""
        avg = round(grade["avg"], 1)
    comments = Spotcomment.objects.filter(spot=spot)
    context = {
        "spot": spot,
        "comment_form": comment_form,
        "comments": comments,
        "avg": avg,
        "star": star,
    }
    return render(request, "places/spot.html", context)


@login_required
def createspot(request, cityname):
    city = City.objects.get(name=cityname)
    if request.method == "POST":
        spot_form = SpotForm(request.POST, request.FILES)
        if spot_form.is_valid():
            spot = spot_form.save(commit=False)
            spot.city = city
            spot.user = request.user
            spot_form.save()
            return redirect("places:city", cityname)

    else:
        spot_form = SpotForm()

    context = {
        "spot_form": spot_form,
    }

    return render(request, "places/createspot.html", context)


@login_required
def deletespot(request, cityname, pk):
    Spot.objects.get(pk=pk).delete()
    return redirect("places:city", cityname)


@login_required
def updatespot(request, cityname, pk):
    spot = Spot.objects.get(pk=pk)
    if request.method == "POST":
        spot_form = SpotForm(request.POST, request.FILES, instance=spot)
        if spot_form.is_valid():
            spot_form.save()
            return redirect("places:spot", cityname, pk)
    else:
        spot_form = SpotForm(instance=spot)
    context = {
        "spot_form": spot_form,
    }
    return render(request, "places/createspot.html", context)


@login_required
def spotcomment(request, cityname, pk):
    spot = Spot.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.spot = spot
        comment.user = request.user
        comment.save()
    return redirect("places:spot", cityname, pk)


@login_required
def comment_delete(request, cityname, pk, comment_pk):
    Spotcomment.objects.get(pk=comment_pk).delete()
    return redirect("places:spot", cityname, pk)
