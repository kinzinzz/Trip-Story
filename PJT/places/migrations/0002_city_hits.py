# Generated by Django 3.2.13 on 2022-11-06 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='hits',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
