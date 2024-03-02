from django.conf import settings
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect
import requests
import json
import random

from datetime import datetime

import validators
from django.contrib.auth import (
    login as login_,
)
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse_lazy
from django_filters.views import FilterView
from django.views.generic import View
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from app.filters import (
    ActorFilter,
    DirectorFilter, 
    MovieFilter,
)

from app.forms import  (
    ActorForm, 
    CustomUserChangeForm, 
    DirectorForm, 
    MovieForm,
)
from app.mixins import CustomLoginRequiredMixin, RegularUserReadOnlyFormMixin, SuperuserPermissionsOnlyMixin
from app.models import (
    Movie,
    Actor,
    Director,
)
from app.utils import str2bool


class CustomLoginView(LoginView):
    template_name = 'forms/login.html'
    success_message = 'Hello, %(username)s!'

    def form_valid(self, form):
        messages.success(self.request, self.success_message % form.cleaned_data)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid name or password')
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse_lazy('home')

class CustomRegisterView(FormView):
    template_name = 'forms/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login_(self.request, user)
        messages.success(self.request, f'Hello, {user.username}! You are now registered.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Registration failed. Please check the form.')
        return super().form_invalid(form)

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.info(request, 'You are successfully logged out!')
        return response

class SettingsView(CustomLoginRequiredMixin, FormView):
    template_name = 'forms/settings.html'
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('settings')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "You have successfully edited your profile!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error in editing your profile. Please check the form.")
        return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs


def fill_data(request):
    if not request.user.is_superuser:
        messages.error(request, "You haven't permissions for that!")
        return redirect(reverse_lazy('home'))
    
    MAX_PAGE_TMDB = 500
    
    req_data = {
        'url': 'https://api.themoviedb.org/3/movie/popular?language=en-US',
        'params': {
            'api_key': settings.TMDB_API_KEY,
            'page': random.randint(1, MAX_PAGE_TMDB)
        }
    }
    

    data_tmdb = requests.get(**req_data)
    with open ('log.txt', 'a+') as f:
       f.write(f"\n\n\nEEEEEEE {data_tmdb.text}\n\n\n") 
    data_tmdb = data_tmdb.json()
     
    req_data = {
        'url': 'http://www.omdbapi.com/',
        'params': {
            'apikey': settings.OMDB_API_KEY,
            'r': 'json',
        }
    }
    

    for movie_tmdb in data_tmdb.get('results'): 
        req_data['params']['t'] = movie_tmdb.get('title') # title like a search query

        movie_omdb = requests.get(**req_data).json()
        if str2bool(movie_omdb.get('Response', 'false')): # if has response
            naming_fields = ['name', 'surname']

            director_naming = dict(
                zip(
                    naming_fields, 
                    movie_omdb.get('Director').split(maxsplit=1)
                )
            )
            director, created = Director.objects.get_or_create(
                defaults={
                    'date_of_birth': None,
                    **director_naming
                },
                **director_naming,
            )
            
            actors = []
            for actor_naming in movie_omdb.get('Actors').split(', '):
                actor_naming = dict(
                    zip(
                        naming_fields, 
                        actor_naming.split(maxsplit=1)
                    )
                )
                
                actor, created = Actor.objects.get_or_create(
                    defaults={
                        'date_of_birth': None,
                        **actor_naming
                    },
                    **actor_naming,
                )
                
                actors.append(actor)
            try:
                movie_release_date = datetime.strptime(movie_omdb.get('Released'), '%d %b %Y')
            except:
                movie_release_date = datetime.strptime(movie_omdb.get('Year'), "%Y")
            
            logo_url = movie_omdb.get('Poster')
            
            if not validators.url(logo_url): # not valid url
                logo_url = None
                
            movie_info = {
                'title': movie_omdb.get('Title'),
                'release_date': movie_release_date,
                'director': director,
            }

            movie, created = Movie.objects.get_or_create(
                defaults={
                    'logo_url': logo_url,
                    **movie_info
                },
                actors__in = actors,
                **movie_info
            )
            if created:
                movie.actors.set(actors)


    return HttpResponse("Data filled from OMDB API")

def delete_data(request):
    if not request.user.is_superuser:
        messages.error(request, "You haven't permissions for that!")
        return redirect(reverse_lazy('home'))
    Director.objects.all().delete()
    Actor.objects.all().delete()
    Movie.objects.all().delete()
    
    return HttpResponse("Movies data totally removed")

class ActorsListView(CustomLoginRequiredMixin, FilterView):
    model = Actor
    filterset_class = ActorFilter
    template_name = 'actors_list.html'
    context_object_name = 'actors'
    paginate_by = 25
    
class ActorAddView(CustomLoginRequiredMixin, SuperuserPermissionsOnlyMixin, FormView):
    template_name = 'forms/actor.html'
    form_class = ActorForm
    success_url = reverse_lazy('actors_list')
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, "You are successfully added a new actor!")
        return super().form_valid(form)   
     
class ActorEditView(CustomLoginRequiredMixin, RegularUserReadOnlyFormMixin, FormView):
    template_name = 'forms/actor.html'
    form_class = ActorForm
    success_url = reverse_lazy('actors_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = get_object_or_404(Actor, pk=self.kwargs['id'])

        return kwargs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['editing'] = True
        return context
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, f"You are successfully edited actor '{form.instance}'!")
        return super().form_valid(form)


class ActorDeleteView(CustomLoginRequiredMixin, SuperuserPermissionsOnlyMixin, View):
    def get(self, request, id):
        actor = get_object_or_404(Actor, pk=id)
        actor.delete()
        messages.success(request, f"You have successfully deleted actor '{actor}' !")
        return redirect('actors_list')

class DirectorsListView(CustomLoginRequiredMixin, FilterView):
    model = Director
    filterset_class = DirectorFilter
    template_name = 'directors_list.html'
    context_object_name = 'directors'
    paginate_by = 25

class DirectorAddView(CustomLoginRequiredMixin, SuperuserPermissionsOnlyMixin, FormView):
    template_name = 'forms/director.html'
    form_class = DirectorForm
    success_url = reverse_lazy('directors_list')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "You are successfully added a new director!")
        return super().form_valid(form)   
     
class DirectorEditView(CustomLoginRequiredMixin, RegularUserReadOnlyFormMixin, FormView):
    template_name = 'forms/director.html'
    form_class = DirectorForm
    success_url = reverse_lazy('directors_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = get_object_or_404(Director, pk=self.kwargs['id'])
        
        return kwargs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['editing'] = True
        
        return context
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, f"You are successfully edited director '{form.instance}'!")
        return super().form_valid(form)

class DirectorDeleteView(CustomLoginRequiredMixin, SuperuserPermissionsOnlyMixin, View):
    def get(self, request, id):
        director = get_object_or_404(Director, pk=id)
        director.delete()
        messages.success(request, f"You have successfully deleted director '{director}' !")
        return redirect('directors_list')

class HomeView(CustomLoginRequiredMixin, FilterView):
    model = Movie
    template_name = 'home.html'
    context_object_name = 'movies'
    filterset_class = MovieFilter
    ordering = ['-release_date']
    paginate_by = 25

class MovieAddView(CustomLoginRequiredMixin, SuperuserPermissionsOnlyMixin, FormView):
    template_name = 'forms/movie.html'
    form_class = MovieForm
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, "You are successfully added a new movie!")
        return super().form_valid(form)

class MovieEditView(CustomLoginRequiredMixin, RegularUserReadOnlyFormMixin, FormView):
    template_name = 'forms/movie.html'
    form_class = MovieForm
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = get_object_or_404(Movie, pk=self.kwargs['id'])

        return kwargs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['editing'] = True
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, f"You are successfully edited movie '{form.instance}'!")
        return super().form_valid(form)
    
class MovieDeleteView(CustomLoginRequiredMixin, SuperuserPermissionsOnlyMixin, View):
    def get(self, request, id):
        movie = get_object_or_404(Movie, pk=id)
        movie.delete()
        messages.success(request, f"You have successfully deleted movie '{movie}' !")
        return redirect('home')
