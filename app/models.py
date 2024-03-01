from django.apps import apps
from django.db import models
import uuid


app_label = apps.get_containing_app_config(__name__).label
          
class Actor(models.Model):
    id                 = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name               = models.CharField(max_length=64, db_index=True)
    surname            = models.CharField(max_length=64, db_index=True)
    date_of_birth      = models.DateField(db_index=True, null=True, blank=True)

    class Meta:
        indexes = [
           models.Index(fields=['name', 'surname',]),
        ]
        
    def __str__(self):
        return f" {self.name} {self.surname}"

class Director(models.Model):
    id                 = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name               = models.CharField(max_length=64, db_index=True)
    surname            = models.CharField(max_length=64, db_index=True)
    date_of_birth      = models.DateField(db_index=True, null=True, blank=True)

    class Meta:
        indexes = [
           models.Index(fields=['name', 'surname',]),
        ]
        
    def __str__(self):
        return f"{self.name} {self.surname}"
    

class Movie(models.Model):
    id                 = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title              = models.CharField(max_length=64, db_index=True)
    logo_url           = models.URLField(max_length = 200, null=True, blank=True)
    release_date       = models.DateField(max_length=64, db_index=True)
    director           = models.ForeignKey(Director, on_delete=models.CASCADE)
    actors             = models.ManyToManyField(Actor, through='MovieActorRelation')
    
    class Meta:
        indexes = [
           models.Index(fields=['title', 'release_date',]),
           models.Index(fields=['title', 'release_date', 'director']),
        ]
        
    def __str__(self):
        return f"{self.director}: {self.title} ({self.release_date.year})"

class MovieActorRelation(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Movie Actor"
        verbose_name_plural = "Movie Actor"
        
        db_table = app_label + '_movie_actor_relation'
        indexes = [
            models.Index(fields=['movie', 'actor']),
        ]
