# To launch the server with Uvicorn, write uvicorn main:app --reload
from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer

app = FastAPI()
app.title = 'My Movie API'
app.version = '0.0.1'

# We use Basemodel for modeling classes in fastapi, this way we can reuse th class instead of writing in each HTTP request the fields we need.
# Also Optional from Typing module was imported for marking attribute id as optional
# Using Field class, we can make some validations like max/min lenght, default values, etc...


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != 'admin@mail.com':
            raise HTTPException(status_code=403, detail='Invalid credentials')


class User(BaseModel):
    email: str
    password: str


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(max_length=15, min_length=1, default='Movie')
    year: int
    rating: float

    # We can also put the default values in a class Config
    class Config:
        schema_extra = {
            'example': {
                'id': 1,
                'title': 'The Matrix',
                'year': 2019,
                'rating': 8.5
            }
        }


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


@app.get('/movies', tags=['movies'], dependencies=[Depends(JWTBearer())])
def get_movies():
    return JSONResponse(content=movies)

# Get with url parameter
# We can import the PATH class from fastapi to validate the route parameters


@app.get('/movies/{id}', tags=['movies'])
def get_movie(id: int = Path(ge=1, le=2000)):
    movie = list(filter(lambda x: x['id'] == id, movies))
    return JSONResponse(content=movie)

# Get with query parameter
# Also we can validate Query parameters importing the class Query from Fastapi


@app.get('/movies/', tags=['movies'])
def get_movies_by_year(year: int = Query(ge=1800, le=2023)):
    years_movies = list(filter(lambda x: x['year'] == year, movies))
    return JSONResponse(content=years_movies)


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
    return JSONResponse(content={'message': 'Movie created successfully'})

# Simple put. Update the movie
# We can also apply Modelbase class in the puts


@app.put('/movies/{id}', tags=['movies'])
def update_movie(id: int, movie: Movie):
    mov = list(filter(lambda x: x['id'] == id, movies))
    mov[0]['title'] = movie.title
    mov[0]['year'] = movie.year
    mov[0]['rating'] = movie.rating
    return JSONResponse(content={'message': 'Movie updated successfully'})

# Simple delete. Delete a movie


@app.delete('/movies/{id}', tags=['movies'])
def delete_movie(id: int):
    movie = list(filter(lambda x: x['id'] == id, movies))
    movies.remove(movie[0])
    return JSONResponse(content={'message': 'Movie deleted successfully'})

# Authorization using PyJWT


@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == 'admin@mail.com' and user.password == 'password':
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)
    else:
        return JSONResponse(status_code=401, content={'message': 'Invalid credentials'})


if __name__ == '__main__':
    message()
