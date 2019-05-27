from rest_framework import serializers
from .models import Comment, Movie


class FetchMovieSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class MovieRankingSerializer(serializers.Serializer):
    movie_id = serializers.IntegerField(source='id')
    total_comments = serializers.IntegerField()
    rank = serializers.IntegerField()


class CommentSerializer(serializers.ModelSerializer):
    movie_id = serializers.IntegerField()
    class Meta:
        model = Comment
        exclude = ('publication_time', 'movie')
