# Generated by Django 4.1.7 on 2023-02-22 04:28

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('netflix_backend_api', '0006_episode_episode_slug_season_season_slug_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='season',
            name='episode',
        ),
        migrations.AddField(
            model_name='episode',
            name='season',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='netflix_backend_api.season'),
        ),
        migrations.AlterField(
            model_name='media',
            name='release_date',
            field=models.DateField(default=datetime.datetime(2023, 2, 22, 4, 28, 18, 968649, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='trailer',
            name='release_date',
            field=models.DateField(default=datetime.datetime(2023, 2, 22, 4, 28, 18, 968649, tzinfo=datetime.timezone.utc)),
        ),
    ]
