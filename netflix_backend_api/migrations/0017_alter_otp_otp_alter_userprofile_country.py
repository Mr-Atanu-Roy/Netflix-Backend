# Generated by Django 4.1.7 on 2023-02-22 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netflix_backend_api', '0016_alter_media_release_date_alter_otp_otp_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='otp',
            field=models.CharField(default='169667', max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='country',
            field=models.CharField(blank=True, default='india', max_length=255, null=True, verbose_name='Country'),
        ),
    ]
