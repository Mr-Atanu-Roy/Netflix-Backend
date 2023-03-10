# Generated by Django 4.1.7 on 2023-02-23 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netflix_backend_api', '0022_alter_cast_movie'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='poster',
        ),
        migrations.AddField(
            model_name='movie',
            name='poster1',
            field=models.FileField(max_length=600, null=True, upload_to='movie/poster/', verbose_name='Movie Pster 1'),
        ),
        migrations.AddField(
            model_name='movie',
            name='poster2',
            field=models.FileField(blank=True, max_length=600, null=True, upload_to='movie/poster/', verbose_name='Movie Pster 2'),
        ),
    ]
