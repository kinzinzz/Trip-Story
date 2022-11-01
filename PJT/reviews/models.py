from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.db import models
from django.contrib.auth import get_user_model
import datetime
# Create your models here.




class Review(models.Model):
    # place = models.ForeignKey()
    # like = models.ForeignKey(User, related_name='UserLike', on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    subtitle = models.CharField(max_length=80)
    content = models.TextField()
    image = ProcessedImageField(upload_to='media/', blank=True,
                                processors=[ResizeToFill(400,500)],
                                format='JPEG',
                                options={'quality': 80})
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now = True)
    start_day = models.DateField(default=datetime.date.today, help_text="날짜 및 시간")
    end_day = models.DateField(default=datetime.date.today, help_text="날짜 및 시간")
    # user = models.ForeignKey(User, related_name='UserName', on_delete=models.CASCADE)
    