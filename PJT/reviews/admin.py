from django.contrib import admin
from .models import Review

# Register your models here.


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "content",
        "subtitle",
        "title",
        "image",
        "created_at",
        "modified_at",
        "start_day",
        "end_day",
    )


admin.site.register(Review)
