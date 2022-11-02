from django.shortcuts import render, redirect
from .models import City, Place
from .forms import CityForm
from django.contrib.auth.decorators import login_required

# Create your views here.


def inform(request):
citys = City.objects.all()
    context = {
        "citys": citys,
    }
    return render(request, "places/inform.html", context)

def place(request):
  return render(request, 'places/place.html')


def city(request, cityname):
    city = City.objects.get(name=cityname)
    context = {
        "city": city,
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
