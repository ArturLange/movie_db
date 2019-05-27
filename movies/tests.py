from django.test import TestCase, Client
from unittest.mock import Mock, patch
from .models import Movie
import json


movie_object = json.loads(
    '{"Title":"Avengers: Endgame","Year":"2019","Rated":"PG-13","Released":"26 Apr 2019","Runtime":"181 min","Genre":"Action, Adventure, Fantasy, Sci-Fi","Director":"Anthony Russo, Joe Russo","Writer":"Christopher Markus, Stephen McFeely, Stan Lee (based on the Marvel comics by), Jack Kirby (based on the Marvel comics by), Jim Starlin (comic book)","Actors":"Robert Downey Jr., Chris Evans, Mark Ruffalo, Chris Hemsworth","Plot":"After the devastating events of Avengers: Infinity War (2018), the universe is in ruins. With the help of remaining allies, the Avengers assemble once more in order to undo Thanos\' actions and restore order to the universe.","Language":"English, Japanese, Xhosa","Country":"USA","Awards":"N/A","Poster":"https://m.media-amazon.com/images/M/MV5BMTc5MDE2ODcwNV5BMl5BanBnXkFtZTgwMzI2NzQ2NzM@._V1_SX300.jpg","Ratings":[{"Source":"Internet Movie Database","Value":"8.9/10"},{"Source":"Rotten Tomatoes","Value":"95%"},{"Source":"Metacritic","Value":"78/100"}],"Metascore":"78","imdbRating":"8.9","imdbVotes":"360,133","imdbID":"tt4154796","Type":"movie","DVD":"N/A","BoxOffice":"N/A","Production":"Marvel Studios","Website":"https://movies.disney.com/avengers-endgame","Response":"True"}')


def load_movies():
    with open('movies.json') as json_file:
        movies_json = json.load(json_file)
    for movie in movies_json:
        Movie(**movie).save()


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    return MockResponse(movie_object, 200)


class TestMovieCreationViews(TestCase):

    @patch('movies.views.requests.get', side_effect=mocked_requests_get)
    def test_movie_is_created(self, get_mock):
        self.assertEqual(Movie.objects.all().count(), 0)
        c = Client()
        response = c.post('/movies', {"title": "Avengers Endgame"})
        self.assertEqual(Movie.objects.all().count(), 1)
        response_data = response.json()
        self.assertEqual(response_data['title'], "Avengers: Endgame")

    @patch('movies.views.requests.get', side_effect=mocked_requests_get)
    def test_movie_is_updated(self, get_mock):
        self.assertEqual(Movie.objects.all().count(), 0)
        c = Client()

        response = c.post('/movies', {"title": "Avengers Endgame"})
        self.assertEqual(Movie.objects.all().count(), 1)
        movie_id = Movie.objects.first().id

        movie = Movie.objects.first()
        movie.title = "Captain America"
        movie.save()

        response = c.post('/movies', {"title": "Avengers Endgame"})
        self.assertEqual(Movie.objects.all().count(), 1)
        self.assertEqual(Movie.objects.first().id, movie_id)

        response_data = response.json()
        self.assertEqual(response_data['title'], "Avengers: Endgame")

    def test_get_movies(self):
        load_movies()
        c = Client()
        response = c.get('/movies')
        self.assertEqual(Movie.objects.all().count(), 5)
