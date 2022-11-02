from django.db import models
from django.contrib.auth import get_user_model
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
import datetime

# User 모델 가져오기
User = get_user_model()


class Review(models.Model):

    """
    N:M 도시
    city = models.ForeignKey(
        models.city, related_name="review_city", on_delete=models.CASCADE
    )
    """

    city_choices = [
        (None, "선택"),
        ("서울", "서울"),
        ("제주", "제주"),
        ("부산", "부산"),
    ]
    city = models.CharField(max_length=2, choices=city_choices, default="선택")

    # )

    # 좋아요
    like = models.ManyToManyField(User, related_name="review_like", blank=True)

    # 리뷰 내용
    content = models.TextField()

    # 리뷰제목
    title = models.CharField(max_length=80)

    # 부제
    subtitle = models.CharField(max_length=80)

    # 이미지
    image = ProcessedImageField(
        upload_to="media/",
        blank=True,
        processors=[ResizeToFill(300, 400)],
        format="JPEG",
        options={"quality": 60},
    )

    # 작성시간
    created_at = models.DateTimeField(auto_now_add=True)

    # 수정시간
    modified_at = models.DateTimeField(auto_now=True)

    # 여행 일정 시작일
    start_day = models.DateField(default=datetime.date.today, help_text="날짜 및 시간")

    # 여행 일정 종료일
    end_day = models.DateField(default=datetime.date.today, help_text="날짜 및 시간")

    # 리뷰 작성자
    user = models.ForeignKey(User, related_name="review_user", on_delete=models.CASCADE)
