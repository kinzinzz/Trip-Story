from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
import datetime
from places.models import City

# User 모델 가져오기
User = get_user_model()


class Review(models.Model):

    # 테마
    THEME_CHOICES = (
        (None, "선택"),
        ("나홀로여행", "나홀로여행"),
        ("친구와함께", "친구와함께"),
        ("커플여행", "커플여행"),
        ("비즈니스여행", "비즈니스여행"),
        ("가족여행", "가족여행"),
    )
    themes = models.CharField(max_length=10, choices=THEME_CHOICES, default="")

    # 리뷰 도시들
    city = models.ManyToManyField(City, related_name="review_city", blank=True)

    # 좋아요
    like = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="review_like", blank=True
    )

    # 리뷰 내용
    content = models.TextField()

    # 리뷰제목
    title = models.CharField(max_length=80)

    # 부제
    subtitle = models.CharField(max_length=80)

    # 썸네일 이미지
    thumbnail_image = ProcessedImageField(
        upload_to="media/",
        blank=True,
        processors=[ResizeToFill(300, 400)],
        format="JPEG",
        options={"quality": 60},
    )
    # 리뷰 이미지
    review_image = ProcessedImageField(
        upload_to="media/",
        blank=True,
        processors=[ResizeToFill(720, 480)],
        format="JPEG",
        options={"quality": 100},
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # 리뷰 조회수
    hits = models.PositiveIntegerField(default=0)

    @property
    def update_hits(self):
        self.hits = self.hits + 1
        self.save()
