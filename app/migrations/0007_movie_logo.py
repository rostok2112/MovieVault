# Generated by Django 5.0.2 on 2024-03-01 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_rename_movie_actor_movie_i_87b358_idx_app_movie_a_movie_i_e575a8_idx_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]
