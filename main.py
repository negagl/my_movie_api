# To launch the server with Uvicorn, write uvicorn main:app --reload
from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
app.title = 'My Movie API'
app.version = '0.0.1'

# We use Basemodel for modeling classes in fastapi, this way we can reuse th class instead of writing in each HTTP request the fields we need.
# Also Optional from Typing module was imported for marking attribute id as optional


class Movie(BaseModel):
    id: Optional[int] = None
    title: str
    year: int
    rating: float


movies = [
    {
        'id': 1,
        'title': 'The Matrix',
        'year': 2019,
        'rating': 8.5
    },
    {
        'id': 2,
        'title': 'Avatar',
        'year': 2000,
        'rating': 8.5
    },
    {
        'id': 3,
        'title': 'Winnie the pooh',
        'year': 1888,
        'rating': 8.5
    }
]

# Home route


@app.get('/', tags=['home'])
def message():
    return 'hello world'

# Simple get


@app.get('/movies', tags=['movies'])
def get_movies():
    return movies

# Get with url parameter


@app.get('/movies/{id}', tags=['movies'])
def get_movie(id: int):
    movie = list(filter(lambda x: x['id'] == id, movies))
    return movie

# Get with query parameter


@app.get('/movies/', tags=['movies'])
def get_movies_by_category(year: int):
    movie = list(filter(lambda x: x['year'] == year, movies))
    return movie


# Simple post
# We have to import Body from fastapi
# OLD POST, BEFORE BASEMODEL

# @app.post('/movies', tags=['movies'])
# def create_movie(id: int = Body(), title: str = Body(), year: int = Body(), rating: float = Body()):
#     new_movie = {'id': id, 'title': title, 'year': year, 'rating': rating}
#     movies.append(new_movie)
#     return new_movie

# New POST method using BaseModel class
@app.post('/movies', tags=['movies'])
def create_movie(movie: Movie):
    movies.append(movie)
    return movie

# Simple put. Update the movie
# We can also apply Modelbase class in the puts


@app.put('/movies/{id}', tags=['movies'])
def update_movie(id: int, movie: Movie):
    movie = list(filter(lambda x: x['id'] == id, movies))
    movie[0]['title'] = movie.title
    movie[0]['year'] = movie.year
    movie[0]['rating'] = movie.rating
    return movie


# Simple delete. Delete a movie
@app.delete('/movies/{id}', tags=['movies'])
def delete_movie(id: int):
    movie = list(filter(lambda x: x['id'] == id, movies))
    movies.remove(movie[0])
    return movie


if __name__ == '__main__':
    message()
