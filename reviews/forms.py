from importlib.resources import contents
from . import models
from django import forms
from django.forms.widgets import NumberInput
from places.models import City


class CustomMMCF(forms.ModelMultipleChoiceField):
    def label_from_instance(self, city):
        return city.name


# 도시 선택
THEME_CHOICES = (
    (None, "선택"),
    ("나홀로여행", "나홀로여행"),
    ("친구와함께", "친구와함께"),
    ("커플여행", "가족여행"),
    ("비즈니스여행", "비즈니스여행"),
    ("가족여행", "가족여행"),
)

# 리뷰 작성폼
class ReviewForm(forms.ModelForm):

    city = CustomMMCF(queryset=City.objects.all(), widget=forms.CheckboxSelectMultiple)

    themes = forms.ChoiceField(label="테마 선택", choices=THEME_CHOICES, required=True)

    title = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "리뷰 제목을 입력하세요",
            }
        ),
    )

    subtitle = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "부재를 입력하세요",
            }
        ),
    )

    start_day = forms.DateTimeField(
        widget=NumberInput(attrs={"type": "date"}), label="일정시작일"
    )

    end_day = forms.DateTimeField(
        widget=NumberInput(attrs={"type": "date"}), label="일정종료일"
    )

    class Meta:
        model = models.Review
        fields = (
            "city",
            "themes",
            "title",
            "subtitle",
            "content",
            "thumbnail_image",
            "review_image",
            "start_day",
            "end_day",
        )

        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 10,
                    "placeholder": "리뷰내용을 입력하세요",
                },
            ),
        }
        labels = {"content": "", "thumbnail_image": "썸네일 이미지", "review_image": "리뷰 이미지"}
