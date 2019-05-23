from django.urls import path

from . import views

urlpatterns = [
    path('movies', views.ListMovies.as_view(), name='movies'),
    path('comments', views.Comments.as_view(), name='comments'),
]
