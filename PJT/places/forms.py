from django import forms
from .models import City, Spot, Spotcomment
from .widgets import starWidget


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


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "댓글을 남겨보세요 💬",
            }
        ),
    )

    class Meta:
        model = Spotcomment
        fields = [
            "content",
            "grade",
        ]
        labels = {
            "grade": "",
        }
        widgets = {
            "grade": starWidget,
        }
