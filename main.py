from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse,RedirectResponse, FileResponse
from pydantic import BaseModel, Field, field_validator, ValidationError

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
    title: str 
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=datetime.date.today().year, ge=2000)
    rating: float = Field(ge=0, le=10)
    category: str = Field(min_length=5, max_length=20)

    @field_validator('title') # Especifica el campo a validar
    @classmethod # Obligatorio en Pydantic v2
    def must_not_be_unknown(cls, value):
    # Primero se ejecutan las validaciones de Field (min_length=5), 
        # luego se ejecuta esta lógica.
        if len(value) < 5:
        # Para errores personalizados, lanzamos ValueError
            raise ValueError('title field must have a minium length of 5 chaterectrs')
        if len(value) > 15:
            raise ValueError('title field must have a maxium length of 5 chaterectrs')
        # Siempre se debe retornar el valor validado
        return value


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
    return PlainTextResponse(content='Home', status_code=200)


@app.get('/movies', tags=['homee'])
def get_movie() -> List[Movie]:
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=200)

@app.get('/movies/{id}', tags=['Movies_1'])
def get_movie(id: int = Path(gt=0)) -> Movie | dict:
    for movie in movies:
        if movie.id == id: 
            return JSONResponse(movie.model_dump(), status_code=200)
    return JSONResponse(content={}, status_code=404)

# localhost:5000/movies/2 (esto es lo que estamos haciendo)
# localhost:5000/movies/?id=2 (este va con clave y valor)
#la dependencia body le dice a fastapi que esto no es un query osea que no va ir en la url como por ejemplo:/movies/1?title=Matrix. sino que va en el cuerpo de json no que ira en path osea datos de ruta como /movies/{id}.
#(IMPORTANTE PARA QUE ESTE NO SE CONFUNDA CON EL PARAMETROS PONERELE (''/movies/)     es importante diferenciarlo por / para que la quary este despues de /)

@app.get('/movies/', tags=['Movies_1'])
def get_movie_by_category(category: str = Query(min_length=5, max_length= 20)) -> Movie | dict:
    for movie in movies:
        if movie.category == category:
            return JSONResponse(movie.model_dump(), status_code=200)
    return JSONResponse(content={}, status_code=404)

#DATOS QUE QUEREMOS INCERTAR

@app.post('/movies', tags=['Movies_1'])
def create_movie(movie: MovieCreate) -> List[Movie]:

    #metodo append es para incertar al final de la lista
    movies.append(movie)
    #lo volvemos un dicicionario apra que pueda ser inseritado dentro de la lista de peliculas 
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=201)

    #return RedirectResponse('/movies', status_code=303)


#parametro del tipo pad
@app.put('/movies/{id}', tags=['Movies_1'])
def update_movie(id: int, movie: MovieUpdate) -> List[Movie]:
    for item in movies:
        if item.id == id:
            item.title = movie.title
            item.overview = movie.overview
            item.year = movie.year
            item.rating = movie.rating
            item.category = movie.category
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=200)


@app.delete('/movies/{id}', tags=['Movies_1'])
def delate_movie(id: int) -> List[Movie]:
    for movie in movies:
        if movie.id == id:
            movies.remove(movie)
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=200)

@app.get('/get_file')
def get_file():
    return FileResponse("chica.jpg")