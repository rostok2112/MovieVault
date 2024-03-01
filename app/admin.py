from datetime import datetime
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from app.models import (
   Movie, Actor, Director
)


class MovieDirectorInline(admin.TabularInline):
    verbose_name = "Movie"
    model = Movie
    extra = 0
    
    readonly_fields = ['logo_preview']
        
    def logo_preview(self, obj):
        out = f'<img src="{obj.logo_url}" style="max-height: 100px; max-width: 100px;" />'
        return mark_safe(out)

class MovieActorInline(admin.TabularInline):
    verbose_name = "Movie"
    model = Movie.actors.through
    extra = 0
    
    readonly_fields = ['title', 'release_date', 'director', 'logo_preview']
    
    def title(self, obj):
        return obj.movie.title
    
    def release_date(self, obj):
        return obj.movie.release_date
    
    def director(self, obj):
        director = obj.movie.director
        
        if director:
            url = reverse('admin:%s_%s_change' % (director._meta.app_label, director._meta.model_name), args=[director.pk])
            return mark_safe(f'<a href="{url}">{director}</a>')
    
    def logo_preview(self, obj):
        out = f'<img src="{obj.movie.logo_url}" style="max-height: 100px; max-width: 100px;" />'
        return mark_safe(out)
                                        
class ActorMovieInline(admin.TabularInline):
    verbose_name = "Actor"
    model = Movie.actors.through
    extra = 0
    
    readonly_fields = ['name', 'surname', 'date_of_birth', 'age']
    
    def name(self, obj):
        return obj.actor.name
    
    def surname(self, obj):
        return obj.actor.surname
    
    def date_of_birth(self, obj):
        return obj.actor.date_of_birth or '-'
    
    def age(self, obj):
        return datetime.today().year - obj.actor.date_of_birth.year

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
   inlines = [MovieActorInline]
   readonly_fields = ('age',)
   
   def age(self, obj):
        return datetime.today().year - obj.date_of_birth.year

@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
   inlines = [MovieDirectorInline]
   readonly_fields = ('age',)
   def age(self, obj):
        return datetime.today().year - obj.date_of_birth.year
    
   def get_inline_instances(self, request, obj=None):
        if obj:
            return super().get_inline_instances(request, obj)
        else:
            return []

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    inlines = [ActorMovieInline]
    readonly_fields = ('logo_preview',)

    def logo_preview(self, obj):
        out = f'<img src="{obj.logo_url}" style="max-height: 100px; max-width: 100px;" />'
        return mark_safe(out)