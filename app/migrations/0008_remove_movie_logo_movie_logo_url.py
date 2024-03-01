# Generated by Django 5.0.2 on 2024-03-01 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_movie_logo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='logo',
        ),
        migrations.AddField(
            model_name='movie',
            name='logo_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
