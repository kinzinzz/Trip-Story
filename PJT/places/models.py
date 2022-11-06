from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

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
        processors=[ResizeToFill(360, 300)],
        format="JPEG",
        options={"quality": 100},
    )
    image = ProcessedImageField(
        upload_to="places",
        processors=[ResizeToFill(720, 480)],
        format="JPEG",
        options={"quality": 100},
    )


class City(models.Model):
    name = models.CharField(max_length=20)
    thumbnail = ProcessedImageField(
        upload_to="avatars",
        processors=[ResizeToFill(360, 300)],
        format="JPEG",
        options={"quality": 100},
    )
    image1 = ProcessedImageField(
        upload_to="avatars",
        processors=[ResizeToFill(720, 480)],
        format="JPEG",
        options={"quality": 100},
    )
    image2 = ProcessedImageField(
        upload_to="avatars",
        processors=[ResizeToFill(720, 480)],
        format="JPEG",
        options={"quality": 100},
    )
    image3 = ProcessedImageField(
        upload_to="avatars",
        processors=[ResizeToFill(720, 480)],
        format="JPEG",
        options={"quality": 80},
    )
    hits = models.PositiveIntegerField(default=0)

    @property
    def update_hits(self):
        self.hits = self.hits + 1
        self.save()


class Spotcomment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    grade = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
