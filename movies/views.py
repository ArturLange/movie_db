from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Movie


class ListMovies(APIView):

    def get(self, request, format=None):
        movies = Movie.objects.all()
        return Response(movies)
