from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.conf import settings

# Create your models here.
class Spot(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    THEME_CHOICES = (
        ("힐링", "힐링"),
        ("액티비티", "액티비티"),
        ("맛집", "맛집"),
        ("숙박", "숙박"),
        ("체험", "체험"),
    )
    themes = models.CharField(max_length=4, choices=THEME_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    city = models.ForeignKey("City", on_delete=models.CASCADE)
    thumbnail = ProcessedImageField(
        upload_to="places",
        processors=[ResizeToFill(100, 80)],
        format="JPEG",
        options={"quality": 80},
    )
    image = ProcessedImageField(
        upload_to="places",
        processors=[ResizeToFill(720, 480)],
        format="JPEG",
        options={"quality": 80},
    )


class City(models.Model):
    name = models.CharField(max_length=20)
    thumbnail = ProcessedImageField(
        upload_to="avatars",
        processors=[ResizeToFill(100, 80)],
        format="JPEG",
        options={"quality": 80},
    )
    image1 = ProcessedImageField(
        upload_to="avatars",
        processors=[ResizeToFill(720, 480)],
        format="JPEG",
        options={"quality": 80},
    )
    image2 = ProcessedImageField(
        upload_to="avatars",
        processors=[ResizeToFill(720, 480)],
        format="JPEG",
        options={"quality": 80},
    )
    image3 = ProcessedImageField(
        upload_to="avatars",
        processors=[ResizeToFill(720, 480)],
        format="JPEG",
        options={"quality": 80},
    )
