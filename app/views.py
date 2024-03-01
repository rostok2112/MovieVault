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
from django.views.generic import View, ListView
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm

from app.forms import  CustomUserChangeForm
from app.mixins import CustomLoginRequiredMixin
from app.models import (
    Movie,
    Actor,
    Director,
)
from app.utils import str2bool



class HomeView(CustomLoginRequiredMixin, ListView):
    model = Movie
    template_name = 'home.html'
    context_object_name = 'movies'
    ordering = ['-release_date']
    paginate_by = 25


class CustomLoginView(LoginView):
    template_name = 'login.html'
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
    template_name = 'register.html'
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
    template_name = 'settings.html'
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
    MAX_PAGE_TMDB = 500
    
    req_data = {
        'url': 'https://api.themoviedb.org/3/movie/popular?language=en-US',
        'params': {
            'api_key': 'fb46b560646ce1f5e142a20396274fc3',
            'page': random.randint(1, MAX_PAGE_TMDB)
        }
    }
    

    data_tmdb = requests.get(**req_data).json()
     
    req_data = {
        'url': 'http://www.omdbapi.com/',
        'params': {
            'apikey': '7d700d6d',
            'r': 'json',
        }
    }

    for movie_tmdb in data_tmdb['results']: 
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
    Director.objects.all().delete()
    Actor.objects.all().delete()
    Movie.objects.all().delete()
    
    return HttpResponse("Movies data totally removed")