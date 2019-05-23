from rest_framework.views import APIView
from rest_framework.response import Response
from decimal import Decimal
import requests
from datetime import datetime

from .models import Movie, Comment
from .serializers import FetchMovieSerializer, MovieSerializer, CommentSerializer


class ListMovies(APIView):

    def get(self, request, format=None):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = FetchMovieSerializer(request.data)
        title = serializer.data['title']
        movie_data = requests.get(
            f'http://www.omdbapi.com/?apikey=550c2e95&t={title}'
        ).json()
        movie = Movie.objects.filter(imdb_id=movie_data['imdbID']).first()
        if not movie:
            movie = Movie(
                title=movie_data['Title'],
                released_date=datetime.strptime(
                    movie_data['Released'], '%d %b %Y'
                ),
                rated=movie_data['Rated'],
                runtime=int(movie_data['Runtime'][:-4]),
                genre=movie_data['Genre'],
                director=movie_data['Director'],
                writers=movie_data['Writer'],
                actors=movie_data['Actors'],
                plot=movie_data['Plot'],
                language=movie_data['Language'],
                country=movie_data['Country'],
                awards=movie_data['Awards'],
                poster=movie_data['Poster'],
                imdb_id=movie_data['imdbID'],
                imdb_rating=Decimal(movie_data['imdbRating']),
            )
            movie.save()

        movie_serializer = MovieSerializer(movie)

        return Response(movie_serializer.data)


class Comments(APIView):

    def get(self, request, format=None):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        comment = Comment(
            text=request.data['text'],
            movie_id=request.data['movie']
        )
        comment.save()
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
