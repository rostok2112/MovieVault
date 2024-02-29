

# from django.shortcuts import get_object_or_404, redirect
# from django.http import Http404, HttpResponse
from django.contrib.auth import (
    login as login_,
)
from django.contrib import messages
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views.generic import View, ListView
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm



from app.forms import  CustomUserChangeForm
from app.mixins import CustomLoginRequiredMixin

# from app.models import Movie



class HomeView(CustomLoginRequiredMixin, ListView):
    # model = Movies
    template_name = 'home.html'
    context_object_name = 'movies'
    ordering = ['-visit_count']
    paginate_by = 25
    
    def get_queryset(self, *argc, **kwargs):
        return []


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

