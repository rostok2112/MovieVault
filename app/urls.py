from django.urls import path
from django.views.generic.base import RedirectView
from django.urls import reverse_lazy
from app import views


urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("settings", views.SettingsView.as_view(), name="settings"),
    path("login", views.CustomLoginView.as_view(), name="login"),
    path("register", views.CustomRegisterView.as_view(), name="register"),
    path("logout", views.CustomLogoutView.as_view(), name="logout"),
    
    path('api/v1/movies', RedirectView.as_view(url=reverse_lazy("home"), permanent=True),  name="movie_add"),
]
