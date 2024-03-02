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
    
    path('movies/', views.MovieAddView.as_view(),  name="movie_add"),
    path('movies/<uuid:id>/', views.MovieEditView.as_view(),  name="movie_edit"),
    path('movies/<uuid:id>/delete', views.MovieDeleteView.as_view(),  name="movie_delete"),
    
    path('actors_list/', views.ActorsListView.as_view(),  name="actors_list"),
    path('actors/', views.ActorAddView.as_view(),  name="actor_add"),
    path('actors/<uuid:id>/', views.ActorEditView.as_view(),  name="actor_edit"),
    path('actors/<uuid:id>/delete', views.ActorDeleteView.as_view(),  name="actor_delete"),
    path('directors_list/', views.DirectorsListView.as_view(),  name="directors_list"),
    path('directors/', views.DirectorAddView.as_view(),  name="director_add"),
    path('directors/<uuid:id>/', views.DirectorEditView.as_view(),  name="director_edit"),
    path('directors/<uuid:id>/delete', views.DirectorDeleteView.as_view(),  name="director_delete"),
    
    path('api/v1/admin/fill_data', views.fill_data, name="admin_fill_data"),
    path('api/v1/admin/delete_data', views.delete_data, name="admin_delete_data"),
]
