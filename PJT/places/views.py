from django.shortcuts import render, redirect
from .models import City, Spot, Spotcomment
from .forms import CityForm, SpotForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.db.models import Avg

# Create your views here.


def inform(request):
    citys = City.objects.all()
    """
    도시별 날씨
    import requests
            
    city_names = []
    city_name_dict = {
        "서울": "Seoul",
        "부산": "Busan",
        "제주": "Jeju",
        "강릉": "Gangneung",
    }
    
    # 도시를 검색하기위해 영어로 변환(DB에 추가되는대로 dict에 추가)
    for city in citys:
        city_names.append(city_name_dict[city.name])

    weather_data = []
    for city in city_names:
        url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=143e860355ea52d6321d409a05995ecc&lang=kr/"
        city_weather = requests.get(
            url.format(city)
        ).json()
        
        # 영어로 검색한 도시이름 다시 한글로 변환
        reverse_dict = dict(map(reversed, city_name_dict.items()))
        city = reverse_dict[city]

        # city 날씨정보
        weather = {
            "city": city,
            "temperature": city_weather["main"]["temp"],
            "description": city_weather["weather"][0]["description"],
            "icon": city_weather["weather"][0]["icon"],
        }
        
        # city 날씨정보 리스트
        weather_data.append(weather)
      
    """
    context = {
        "citys": citys,
        # "weather_data": weather_data,
    }
    return render(request, "places/inform.html", context)


def place(request):

    return render(request, "places/place.html")


def city(request, cityname):
    city = City.objects.get(name=cityname)
    spots = Spot.objects.filter(city=city)
    cityspots = City.objects.prefetch_related("spot_set").get(name=cityname)
    for cityspot in cityspots:
        print(cityspot.spot_set)
    context = {
        "city": city,
        "spots": spots,
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
def spotcomment(request, cityname, pk):
    spot = Spot.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.spot = spot
        comment.user = request.user
        comment.save()
    return redirect("places:spot", cityname, pk)
