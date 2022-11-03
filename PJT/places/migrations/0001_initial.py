# Generated by Django 3.2.13 on 2022-11-03 01:34

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('thumbnail', imagekit.models.fields.ProcessedImageField(upload_to='avatars')),
                ('image1', imagekit.models.fields.ProcessedImageField(upload_to='avatars')),
                ('image2', imagekit.models.fields.ProcessedImageField(upload_to='avatars')),
                ('image3', imagekit.models.fields.ProcessedImageField(upload_to='avatars')),
            ],
        ),
        migrations.CreateModel(
            name='Spot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('themes', models.CharField(choices=[('힐링', '힐링'), ('액티비티', '액티비티'), ('맛집', '맛집'), ('숙박', '숙박'), ('체험', '체험')], max_length=4)),
                ('thumbnail', imagekit.models.fields.ProcessedImageField(upload_to='places')),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to='places')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='places.city')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Spotcomment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('grade', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('spot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='places.spot')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
