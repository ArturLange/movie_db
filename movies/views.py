from rest_framework.views import APIView
from rest_framework.response import Response
from decimal import Decimal
import requests
from datetime import datetime
from django.db.models import Count, Exists, Q

from .models import Movie, Comment
from .serializers import FetchMovieSerializer, MovieSerializer, CommentSerializer, MovieRankingSerializer


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
                ).date(),
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
        movie_id = request.query_params.get('movie_id')
        comments = Comment.objects.all()
        if movie_id:
            comments = comments.filter(movie_id=movie_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        comment = Comment(
            text=request.data['text'],
            movie_id=request.data['movie_id']
        )
        comment.save()
        serializer = CommentSerializer(comment)
        return Response(serializer.data)


class Ranking(APIView):

    def get(self, request, format=None):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if not start_date or not end_date:
            return Response({'error': 'Needs "start_date" and "end_date" parameters'}, status=400)
        comments_num = Count(
            'comments',
            filter=Q(comments__publication_time__gte=start_date)
        )
        movies = Movie.objects.all().annotate(total_comments=comments_num).order_by('-total_comments')
        ranks = [movie.total_comments for movie in movies]
        for movie in movies:
            movie.rank = ranks.index(movie.total_comments) + 1


        serializer = MovieRankingSerializer(movies, many=True)
        return Response(serializer.data)
