# Generated by Django 5.0.2 on 2024-03-01 02:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_movieactorrelation_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='movieactorrelation',
            options={'verbose_name': 'Movie Actor', 'verbose_name_plural': 'Movie Actor'},
        ),
        migrations.RenameIndex(
            model_name='movieactorrelation',
            new_name='movie_actor_movie_i_87b358_idx',
            old_name='app_movieac_movie_i_5e1e1d_idx',
        ),
        migrations.AlterModelTable(
            name='movieactorrelation',
            table='movie_actor_relation',
        ),
    ]
