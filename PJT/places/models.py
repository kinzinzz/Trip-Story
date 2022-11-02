from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.
class Place(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    THEME_CHOICES = (("힐링", "힐링"), ("액티비티", "액티비티"))
    themes = models.CharField(max_length=4, choices=THEME_CHOICES)
    # user = models.ForeignKey('User', on_delete=models.CASCADE)
    city = models.ForeignKey("City", on_delete=models.CASCADE)


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
