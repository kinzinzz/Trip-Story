from django import forms
from .models import City, Spot


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = "__all__"


class SpotForm(forms.ModelForm):
    class Meta:
        model = Spot
        fields = [
            "title",
            "content",
            "themes",
            "thumbnail",
            "image",
        ]
        labels = {
            "title": "장소명",
            "content": "내용",
            "themes": "테마",
            "thumbnail": "썸네일 사진",
            "image": "이미지",
        }
