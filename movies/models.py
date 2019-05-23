from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=128)
    released_date = models.DateField()
    rated = models.CharField(max_length=32)
    runtime = models.IntegerField()
    genre = models.TextField()
    director = models.TextField()
    writers = models.TextField()
    actors = models.TextField()
    plot = models.TextField()
    language = models.TextField()
    country = models.CharField(max_length=128)
    awards = models.TextField()
    poster = models.URLField()
    imdb_id = models.CharField(max_length=32)
    imdb_rating = models.DecimalField(max_digits=2, decimal_places=1)


class Comment(models.Model):
    text = models.TextField()
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE, related_name='comments'
    )
    publication_time = models.DateTimeField(auto_now_add=True)
