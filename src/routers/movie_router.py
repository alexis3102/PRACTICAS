from typing import List
from fastapi import Path, Query, APIRouter
from fastapi.responses import FileResponse, JSONResponse
from src.models.movie_model import Movie, MovieCreate, MovieUpdate

movies: List[Movie] = []

movie_router = APIRouter()


@movie_router.get('/', tags=['homee'])
def get_movie() -> List[Movie]:
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=200)

@movie_router.get('/by_category', tags=['Movies_1'])
def get_movie_by_category(category: str = Query(min_length=5, max_length= 20)) -> Movie | dict:
    for movie in movies:
        if movie.category == category:
            return JSONResponse(movie.model_dump(), status_code=200)
    return JSONResponse(content={}, status_code=404)


@movie_router.get('/{id}', tags=['Movies_1'])
def get_movie(id: int = Path(gt=0)) -> Movie | dict:
    for movie in movies:
        if movie.id == id: 
            return JSONResponse(movie.model_dump(), status_code=200)
    return JSONResponse(content={}, status_code=404)

# localhost:5000/movies/2 (esto es lo que estamos haciendo)
# localhost:5000/movies/?id=2 (este va con clave y valor)
#la dependencia body le dice a fastapi que esto no es un query osea que no va ir en la url como por ejemplo:/movies/1?title=Matrix. sino que va en el cuerpo de json no que ira en path osea datos de ruta como /movies/{id}.
#(IMPORTANTE PARA QUE ESTE NO SE CONFUNDA CON EL PARAMETROS PONERELE (''/movies/)     es importante diferenciarlo por / para que la quary este despues de /)


#DATOS QUE QUEREMOS INCERTAR

@movie_router.post('/', tags=['Movies_1'])
def create_movie(movie: MovieCreate) -> List[Movie]:

    #metodo append es para incertar al final de la lista
    movies.append(movie)
    #lo volvemos un dicicionario apra que pueda ser inseritado dentro de la lista de peliculas 
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=201)

    #return RedirectResponse('/movies', status_code=303)


#parametro del tipo pad
@movie_router.put('/{id}', tags=['Movies_1'])
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


@movie_router.delete('/{id}', tags=['Movies_1'])
def delate_movie(id: int) -> List[Movie]:
    for movie in movies:
        if movie.id == id:
            movies.remove(movie)
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=200)

@movie_router.get('/get_file')
def get_file():
    return FileResponse("chica.jpg")