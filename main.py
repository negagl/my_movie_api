# To launch the server with Uvicorn, write uvicorn main:app --reload
from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from config.database import Session, Base, engine
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder

app = FastAPI()
app.title = 'My Movie API'
app.version = '0.0.1'

Base.metadata.create_all(bind=engine)


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

# Authorization using PyJWT


@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == 'admin@mail.com' and user.password == 'password':
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)
    else:
        return JSONResponse(status_code=401, content={'message': 'Invalid credentials'})

# Simple get


@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


# Get with url parameter
# We can import the PATH class from fastapi to validate the route parameters
@app.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie_by_id(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': 'Movie not found'})
    # movie = list(filter(lambda x: x['id'] == id, movies))
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


# Get with query parameter
# Also we can validate Query parameters importing the class Query from Fastapi
@app.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_year(year: int = Query(ge=1800, le=2050)) -> List[Movie]:
    # years_movies = list(filter(lambda x: x['year'] == year, movies))
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.year == year).all()
    if not result:
        return JSONResponse(status_code=404, content={'message': 'There are no movies matching the year specified'})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


# Simple post
# We have to import Body from fastapi
# OLD POST, BEFORE BASEMODEL

# @app.post('/movies', tags=['movies'])
# def create_movie(id: int = Body(), title: str = Body(), year: int = Body(), rating: float = Body()):
#     new_movie = {'id': id, 'title': title, 'year': year, 'rating': rating}
#     movies.append(new_movie)
#     return new_movie

# New POST method using BaseModel class
@app.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    # movies.append(movie)
    return JSONResponse(content={'message': 'Movie created successfully'})


# Simple put. Update the movie
# We can also apply Modelbase class in the puts
@app.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    # mov = list(filter(lambda x: x['id'] == id, movies))
    # mov[0]['title'] = movie.title
    # mov[0]['year'] = movie.year
    # mov[0]['rating'] = movie.rating
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': 'Movie not found'})
    result.title = movie.title
    result.year = movie.year
    result.rating = movie.rating
    db.commit()
    return JSONResponse(content={'message': 'Movie updated successfully'})


# Simple delete. Delete a movie
@app.delete('/movies/{id}', tags=['movies'], status_code=200, response_model=dict)
def delete_movie(id: int) -> dict:
    # movie = list(filter(lambda x: x['id'] == id, movies))
    # movies.remove(movie[0])
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': 'Movie not found'})
    db.delete(result)
    db.commit()
    return JSONResponse(content={'message': 'Movie deleted successfully'})


if __name__ == '__main__':
    message()
