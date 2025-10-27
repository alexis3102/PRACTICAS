from fastapi import FastAPI, Response
from fastapi.requests import Request
from fastapi.responses import JSONResponse, PlainTextResponse
from src.routers.movie_router import movie_router

from src.utils.http_error_handler import HTTPErrorHandler



app = FastAPI()

#app.add_middleware(HTTPErrorHandler)

@app.middleware('http')
#asyn ES PARA ESCRIBIR CODIGO ASINCRONO OSEA QUE NO VA LINEA POR LINEA, SI NO QUE ESTA LA EJECUTA EN SEGUNDO PLANO MIENTRAS LAS DEMAS ESPERAN
async def http_error_handler(request:Request, call_next) -> Response | JSONResponse:
    print('middleware is running')
    return await call_next(request)

      
@app.get('/', tags=['homee'])
def homee():
    return PlainTextResponse(content='Home', status_code=200)


app.include_router(prefix='/movies', router=movie_router)


