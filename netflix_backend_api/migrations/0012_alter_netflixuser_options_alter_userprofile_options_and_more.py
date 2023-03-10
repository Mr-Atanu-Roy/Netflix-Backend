# Generated by Django 4.1.7 on 2023-02-22 07:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netflix_backend_api', '0011_rename_trailer_trailer_trailer_url_otp_purpose_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='netflixuser',
            options={'verbose_name_plural': 'Netflix User'},
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name_plural': 'Netflix User Profile'},
        ),
        migrations.AlterField(
            model_name='media',
            name='release_date',
            field=models.DateField(default=datetime.datetime(2023, 2, 22, 7, 12, 50, 972740, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='trailer',
            name='release_date',
            field=models.DateField(default=datetime.datetime(2023, 2, 22, 7, 12, 50, 972740, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.FileField(max_length=600, null=True, upload_to='user/profile', verbose_name='Profile Picture'),
        ),
    ]
