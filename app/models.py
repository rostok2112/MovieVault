from django.db import models
import uuid

class Actor(models.Model):
    id                 = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name               = models.CharField(max_length=64, db_index=True)
    surname            = models.CharField(max_length=64, db_index=True)
    date_of_birth      = models.DateField(max_length=64, db_index=True)

    class Meta:
        indexes = [
           models.Index(fields=['name', 'surname',]),
        ]
        
    def __str__(self):
        return f" {self.name} {self.surname}"

class Producer(models.Model):
    id                 = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name               = models.CharField(max_length=64, db_index=True)
    surname            = models.CharField(max_length=64, db_index=True)
    date_of_birth      = models.DateField(max_length=64, db_index=True)

    class Meta:
        indexes = [
           models.Index(fields=['name', 'surname',]),
        ]
        
    def __str__(self):
        return f"{self.name} {self.surname}"
    
    
class Movie(models.Model):
    id                 = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title              = models.CharField(max_length=64, db_index=True)
    release_date       = models.DateField(max_length=64, db_index=True)
    producer           = models.ForeignKey(Producer, on_delete=models.CASCADE)
    actors             = models.ManyToManyField(Actor)
    
    class Meta:
        indexes = [
           models.Index(fields=['title', 'release_date',]),
        ]
        
    def __str__(self):
        return f"{self.producer}: {self.title}"

