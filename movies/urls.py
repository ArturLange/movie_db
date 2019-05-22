from django.urls import path

from . import views

urlpatterns = [
    path('movies', views.ListMovies.as_view(), name='movies_index'),
]
