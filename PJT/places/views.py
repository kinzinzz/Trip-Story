from django.shortcuts import render, redirect
from .models import City, Spot
from .forms import CityForm, SpotForm
from django.contrib.auth.decorators import login_required

# Create your views here.


def inform(request):
    citys = City.objects.all()
    context = {
        "citys": citys,
    }
    return render(request, "places/inform.html", context)


def place(request):
    return render(request, "places/place.html")


def city(request, cityname):
    city = City.objects.get(name=cityname)
    spots = Spot.objects.filter(city=city)
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
    context = {
        "spot": spot,
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
