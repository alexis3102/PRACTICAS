from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from typing import Optional, List

app = FastAPI()

class Movie(BaseModel):
    id: int
    title: str
    overiew:  str
    year: int
    rating: float
    category: str

class MovieUpdate(BaseModel):
    title: str
    overiew:  str
    year: int
    rating: float
    category: str

movies = [
    {
        "id": 1,
        "title": "tu mama",
        "overiew": "en un exuberante pantalla",
        "year": "2009",
        "rating": 7.8,
        "category": "accion"
    },

    {
        "id": 2,
        "title": "tu papa",
        "overiew": "en un  pantalla",
        "year": "2003",
        "rating": 7.1,
        "category": "horror"
    }
]


@app.get('/', tags=['homee'])
def homee():
    return "hello world"


@app.get('/movies', tags=['homee'])
def get_movie() -> List[Movie]:
    return movies

@app.get('/movies/{id}', tags=['Movies_1'])
def get_movie(id: int) -> Movie:
    for movie in movies:
        if movie['id'] == id:
            return movie
    return[]

# localhost:5000/movies/2 (esto es lo que estamos haciendo)
# localhost:5000/movies/?id=2 (este va con clave y valor)
#la dependencia body le dice a fastapi que esto no es un query osea que no va ir en la url como por ejemplo:/movies/1?title=Matrix. sino que va en el cuerpo de json no que ira en path osea datos de ruta como /movies/{id}.
#(IMPORTANTE PARA QUE ESTE NO SE CONFUNDA CON EL PARAMETROS PONERELE (''/movies/)     es importante diferenciarlo por / para que la quary este despues de /)

@app.get('/movies/', tags=['Movies_1'])
def get_movie_by_category(category: str, year:int)-> Movie:
    for movie in movies:
        if movie['category'] == category:
            return movie
    return[]

#DATOS QUE QUEREMOS INCERTAR

@app.post('/movies', tags=['Movies_1'])
def create_movie(movie: Movie) -> List[Movie]:

    #metodo append es para incertar al final de la lista
    movies.append(movie.model_dump())
    #lo volvemos un dicicionario apra que pueda ser inseritado dentro de la lista de peliculas 
    return movies

#parametro del tipo pad
@app.put('/movies/{id}', tags=['Movies_1'])
def update_movie(id: int, movie: MovieUpdate) -> List[Movie]:
    for items in movies:
        if items['id'] == id:
            items['title'] = movie.title
            items['overiew'] = movie.overiew
            items['year'] = movie.year
            items['rating'] = movie.rating
            items['category'] = movie.category
    return movies

@app.delete('/movies/{id}', tags=['Movies_1'])
def delate_movie(id: int) -> List[Movie]:
    for movie in movies:
        if movie['id'] == id:
            movies.remove(movie)
    return movies