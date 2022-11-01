from django import forms
from .models import Review
from django.forms.widgets import NumberInput

class ReviewForm(forms.ModelForm):
    
    city_choices = [
                (None, "선택"),
                ("서울", "서울"),
                ("제주", "제주"),
                ("부산", "부산"),
        ]
    city = forms.ChoiceField(label="도시", choices=city_choices, required=True)
    start_day = forms.DateTimeField(
        widget=NumberInput(attrs={"type": "date"}), label="일정시작일"
    )

    end_day = forms.DateTimeField(
        widget=NumberInput(attrs={"type": "date"}), label="일정종료일"
    )
    
    class Meta:
        model = Review
        fields = [
            'title','subtitle', 'content', 'image','start_day','end_day'
        ]
       