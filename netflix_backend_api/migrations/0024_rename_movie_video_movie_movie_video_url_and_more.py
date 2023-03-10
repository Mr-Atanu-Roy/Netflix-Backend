# Generated by Django 4.1.7 on 2023-02-23 15:30

import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netflix_backend_api', '0023_remove_movie_poster_movie_poster1_movie_poster2'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='movie_video',
            new_name='movie_video_url',
        ),
        migrations.AlterField(
            model_name='movie',
            name='movie_slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='title', unique=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='poster1',
            field=models.FileField(max_length=600, null=True, upload_to='movie/poster/', verbose_name='Movie Poter 1'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='poster2',
            field=models.FileField(blank=True, max_length=600, null=True, upload_to='movie/poster/', verbose_name='Movie Poter 2'),
        ),
    ]
