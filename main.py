from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from typing import Optional, List
import datetime

app = FastAPI()

class Movie(BaseModel):
    id: int
    title: str
    overview:  str
    year: int
    rating: float
    category: str

class MovieCreate(BaseModel):
    id: int
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=datetime.date.today().year, ge=2000)
    rating: float = Field(ge=0, le=10)
    category: str = Field(min_length=5, max_length=20)

    model_config = {
        'json_schema_extra': {
            'example': {
                'id': 1,
                'title': 'my movie',
                'overview': 'trata sobre........',
                'year': 2022,
                'rating': 5,
                'category': 'comedy'
            }
        }
    }

# gt (greater than) para numeros mayores que.... +
# ge (greater than or aqual) osea mayor o igual..... +=
# lt (less than) menos que..... -
# le (less than or aqual) menor o igual que..... -= 

class MovieUpdate(BaseModel):
    title: str
    overview:  str
    year: int
    rating: float
    category: str

movies: List[Movie] = []


@app.get('/', tags=['homee'])
def homee():
    return "hello world"


@app.get('/movies', tags=['homee'])
def get_movie() -> List[Movie]:
    return [movie.model_dump() for movie in movies]

@app.get('/movies/{id}', tags=['Movies_1'])
def get_movie(id: int) -> Movie:
    for movie in movies:
        if movie['id'] == id:
            return movie.model_dump()
    return[]

# localhost:5000/movies/2 (esto es lo que estamos haciendo)
# localhost:5000/movies/?id=2 (este va con clave y valor)
#la dependencia body le dice a fastapi que esto no es un query osea que no va ir en la url como por ejemplo:/movies/1?title=Matrix. sino que va en el cuerpo de json no que ira en path osea datos de ruta como /movies/{id}.
#(IMPORTANTE PARA QUE ESTE NO SE CONFUNDA CON EL PARAMETROS PONERELE (''/movies/)     es importante diferenciarlo por / para que la quary este despues de /)

@app.get('/movies/', tags=['Movies_1'])
def get_movie_by_category(category: str, year:int)-> Movie:
    for movie in movies:
        if movie['category'] == category:
            return movie.model_dump()
    return[]

#DATOS QUE QUEREMOS INCERTAR

@app.post('/movies', tags=['Movies_1'])
def create_movie(movie: MovieCreate) -> List[Movie]:

    #metodo append es para incertar al final de la lista
    movies.append(movie)
    #lo volvemos un dicicionario apra que pueda ser inseritado dentro de la lista de peliculas 
    return [movie.model_dump() for movie in movies]

#parametro del tipo pad
@app.put('/movies/{id}', tags=['Movies_1'])
def update_movie(id: int, movie: MovieUpdate) -> List[Movie]:
    for item in movies:
        if item['id'] == id:
            item['title'] = movie.title
            item['overiew'] = movie.overiew
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
    return [movie.model_dump() for movie in movies]

@app.delete('/movies/{id}', tags=['Movies_1'])
def delate_movie(id: int) -> List[Movie]:
    for movie in movies:
        if movie['id'] == id:
            movies.remove(movie)
    return [movie.model_dump() for movie in movies]