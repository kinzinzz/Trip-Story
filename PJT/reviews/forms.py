from . import models
from django import forms
from django.forms.widgets import NumberInput

# 도시 선택
city_choices = [
    (None, "선택"),
    ("서울", "서울"),
    ("제주", "제주"),
    ("부산", "부산"),
]

# 리뷰 작성폼
class ReviewForm(forms.ModelForm):
    city = forms.ChoiceField(label="도시", choices=city_choices, required=True)

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
            "title",
            "subtitle",
            "content",
            "image",
            "start_day",
            "end_day",
        )
