from django import forms
import django_filters as filters
from django.core.exceptions import ValidationError
from django.db.models import (
    F, Value, Count,
)
import datetime
from app.models import (
    Movie, Director, Actor,
)

class BaseFilter(filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.date = datetime.date.today()
        
        for filter_ in self.filters: # apply validate_field methods as validators
            validator = getattr(self, "validate_" + filter_, None)
            if validator:
                self.filters[filter_].field.validators.append(validator)

    def age_filter(self, queryset, name, value):
        return (
            queryset
                .annotate(
                    age = Value(self.date.year) - F(name + '__year'),
                )
                .filter(age = value)
        )
    
    def count_filter(self, queryset, name, value):
        return (
            queryset
                .annotate(count = Count(name),)
                .filter(count = value)
        )

class MovieFilter(BaseFilter):
    title = filters.CharFilter(label = "Title", lookup_expr='icontains')
    
    release_date_start = filters.DateFilter(
        field_name='release_date',
        lookup_expr=('gte'),
        label='Release date start',
        widget= forms.DateInput(attrs={'type': 'date'})
    )
    release_date_end = filters.DateFilter(
        field_name='release_date',
        lookup_expr=('lte'),
        label='Release date end',
        widget=forms.DateInput(attrs={'type': 'date',}),
    )
    release_date = filters.NumberFilter(
        field_name='release_date__year', 
        label="Release year", 
    )
    
    count_of_actors = filters.NumberFilter(
        field_name='actors__id',
        label="Count of actors that played in movie",
        method='count_filter',
    )
    
    def validate_year(self, value):
        MIN = 1
        MAX = 9999
        if value < MIN or value > MAX:
            raise ValidationError(f"Year must be in range {MIN} - {MAX}")
    
    def validate_count_of_actors(self, value):
        MIN = 0
        if value < MIN :
            raise ValidationError(f"Count of actors must be more than {MIN}") 
        
    class Meta:
        model = Movie
        fields = ['title', 'director', 'actors']


class ActorFilter(BaseFilter):
    name = filters.CharFilter(label = "Name", lookup_expr='icontains')
    surname = filters.CharFilter(label = "Surname", lookup_expr='icontains')
    
    date_of_birth_start = filters.DateFilter(
        field_name='date_of_birth',
        lookup_expr=('gte'),
        label='Date of birth start',
        widget= forms.DateInput(attrs={'type': 'date',}),
    )
    date_of_birth_end = filters.DateFilter(
        field_name='date_of_birth',
        lookup_expr=('lte'),
        label='Date of birth end',
        widget=forms.DateInput(attrs={'type': 'date',}),
    )
    date_of_birth = filters.NumberFilter(
        field_name='date_of_birth__year', 
        label="Year of birth", 
    )
    
    age = filters.NumberFilter(
        field_name='date_of_birth',
        method='age_filter',
        label="Age", 
    )
    
    movies_count = filters.NumberFilter(
        field_name='movie__id',
        label="Count of movies where actor played",
        method='count_filter',
    )
    
    def validate_year(self, value):
        MIN = 1
        MAX = 9999
        if value < MIN or value > MAX:
            raise ValidationError(f"Year must be in range {MIN} - {MAX}")
     
    def validate_age(self, value):
        MIN = 1
        MAX = 9999
        if value < MIN or value > MAX:
            raise ValidationError(f"Age must be in range {MIN} - {MAX}")  
         
    def validate_movies_count(self, value):
        MIN = 0
        if value < MIN :
            raise ValidationError(f"Movies count must be more than {MIN}")
        
    class Meta:
        model = Actor
        fields = ['name', 'surname', 'date_of_birth']

class DirectorFilter(BaseFilter):
    name = filters.CharFilter(label = "Name", lookup_expr='icontains')
    surname = filters.CharFilter(label = "Surname", lookup_expr='icontains')
    
    date_of_birth_start = filters.DateFilter(
        field_name='date_of_birth',
        lookup_expr=('gte'),
        label='Date of birth start',
        widget= forms.DateInput(attrs={'type': 'date',})
    )
    date_of_birth_end = filters.DateFilter(
        field_name='date_of_birth',
        lookup_expr=('lte'),
        label='Date of birth end',
        widget=forms.DateInput(attrs={'type': 'date',}),
    )
    date_of_birth = filters.NumberFilter(
        field_name='date_of_birth__year', 
        label="Year of birth", 
    )
    
    age = filters.NumberFilter(
        field_name='date_of_birth',
        method='age_filter',
        label="Age", 
    )
    
    movies_count = filters.NumberFilter(
        field_name='movie__id',
        label="Count of movies where actor played",
        method='count_filter',
    )
    
    def validate_year(self, value):
        MIN = 1
        MAX = 9999
        if value < 1 or value > 9999:
            raise ValidationError(f"Year must be in range {MIN} - {MAX}")
     
    def validate_age(self, value):
        MIN = 1
        MAX = 9999
        if value < 1 or value > 9999:
            raise ValidationError(f"Age must be in range {MIN} - {MAX}")
    
    def validate_movies_count(self, value):
        MIN = 0
        if value < MIN :
            raise ValidationError(f"Movies count must be more than {MIN}") 

    class Meta:
        model = Director
        fields = ['name', 'surname', 'date_of_birth']