from django import forms
from .models import Community, Comcomment


class CommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = [
            "title",
            "content",
            "category",
        ]
        labels = {
            "title": "제목",
            "content": "내용",
            "category": "카테고리",
        }


class ComcommentForm(forms.ModelForm):
    content = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "댓글을 남겨보세요 💬",
            }
        ),
    )

    class Meta:
        model = Comcomment
        fields = [
            "content",
        ]
