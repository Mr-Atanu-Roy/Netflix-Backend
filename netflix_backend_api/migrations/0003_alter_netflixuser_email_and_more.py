# Generated by Django 4.1.7 on 2023-02-21 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netflix_backend_api', '0002_alter_netflixuser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='netflixuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name="User's Email Address"),
        ),
        migrations.AlterField(
            model_name='netflixuser',
            name='is_verified',
            field=models.BooleanField(default=False, verbose_name='Is Verified'),
        ),
    ]
