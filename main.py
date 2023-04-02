# To launch the server with Uvicorn, write uvicorn main:app --reload
from fastapi import FastAPI, Body

app = FastAPI()
app.title = 'My Movie API'
app.version = '0.0.1'


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

@app.post('/movies', tags=['movies'])
def create_movie(id: int = Body(), title: str = Body(), year: int = Body(), rating: float = Body()):
    new_movie = {'id': id, 'title': title, 'year': year, 'rating': rating}
    movies.append(new_movie)
    return new_movie


# Simple put. Update the movie
@app.put('/movies/{id}', tags=['movies'])
def update_movie(id: int, title: str = Body(), year: int = Body(), rating: float = Body()):
    movie = list(filter(lambda x: x['id'] == id, movies))
    movie[0]['title'] = title
    movie[0]['year'] = year
    movie[0]['rating'] = rating
    return movie


# Simple delete. Delete a movie
@app.delete('/movies/{id}', tags=['movies'])
def delete_movie(id: int):
    movie = list(filter(lambda x: x['id'] == id, movies))
    movies.remove(movie[0])
    return movie


if __name__ == '__main__':
    message()
