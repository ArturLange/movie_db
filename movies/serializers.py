from rest_framework import serializers
from .models import Comment, Movie


class FetchMovieSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ('publication_time',)