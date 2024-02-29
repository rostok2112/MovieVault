from django.contrib import admin
from app.models import (
   Movie, Actor, Producer
)


class MovieProducerInline(admin.TabularInline):
    verbose_name = "Movie"
    model = Movie
    extra = 0
    
class MovieActorInline(admin.TabularInline):
    verbose_name = "Movie"
    model = Movie.actors.through
    extra = 0
                                        
class ActorMovieInline(admin.TabularInline):
    verbose_name = "Actor"
    model = Movie.actors.through
    extra = 0


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
   inlines = [MovieActorInline]
   
   def get_inline_instances(self, request, obj=None):
        if obj:
            return super().get_inline_instances(request, obj)
        else:
            return []
        
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
   inlines = [ActorMovieInline]
   
   def get_inline_instances(self, request, obj=None):
        if obj:
            return super().get_inline_instances(request, obj)
        else:
            return []

@admin.register(Producer)
class ProducerAdmin(admin.ModelAdmin):
   inlines = [MovieProducerInline]
   
   def get_inline_instances(self, request, obj=None):
        if obj:
            return super().get_inline_instances(request, obj)
        else:
            return []
