# Generated by Django 5.0.2 on 2024-02-29 14:23

from django.db import migrations, models


class Migration(migrations.Migration):
    
    
    dependencies = [
        ('app', '0001_initial'),
    ]

    
        
    operations = [
        migrations.RemoveField(
            model_name='actor',
            name='date_of_birth',
        ),
        migrations.RemoveField(
            model_name='producer',
            name='date_of_birth',
        ),
        migrations.AddField(
            model_name='actor',
            name='date_of_birth',
            field=models.DateField(db_index=True, max_length=64),
        ),
        migrations.AddField(
            model_name='producer',
            name='date_of_birth',
            field=models.DateField(db_index=True, max_length=64),
        ),
    ]
