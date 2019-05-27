# Movie DB

## Setup

1. (optional) create a virtualenv using e.g.

   `virtualenv venv --python=python3`

2. Install dependencies

   `pip install -r requirements.txt`

3. Run migrations

   `./manage.py migrate`

4. Run the application

   `./manage.py runserver`

## Endpoints

- `/movies`

  - `GET` - returns a list of all movies
  - `POST` - accepts a JSON object with `"title"` field - a string to search for in the database.
    Example request:

    ```javascript
    {
      "title": "avatar"
    }
    ```

    A movie found using given string gets written to database and returned.

- `/comments`

  - `GET` - returns a list of all comments in the database. Example response:

    ```javascript
    [
      {
        id: 2,
        movie_id: 1,
        text: "Movie good"
      },
      {
        id: 3,
        movie_id: 2,
        text: "Movie bad"
      }
    ];
    ```

    Also allows filtering by passing the `movie_id` query parameter.

  - `POST` - allows adding a comment to the movie.
    Example request:

    ```javascript
    {
        "text": "Movie not so good",
        "movie_id": 3
    }
    ```

- `/top`

  - `GET` - returns a ranking of most commented movies - requires 2 query parameters - `start_date` and `end_date`, therefore valid url would be something like `/top?start_date=2018-01-01&end_date=2020-01-01`. If parameters are not given returns a 400 Bad Request error.

## Limitations

- At the moment the application uses OMDB - an open movie database which allows only 1000 requests per day.

- Pagination is not implemented, app may become slow if a lot of movies get written.

- App expects OMDB API to be up and running and fails miserably if it's offline.
