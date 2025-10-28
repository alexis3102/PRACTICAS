from fastapi import FastAPI, Query, Response, Depends
from fastapi.requests import Request
from fastapi.responses import JSONResponse, PlainTextResponse
from src.routers.movie_router import movie_router
from src.utils.http_error_handler import HTTPErrorHandler

from fastapi .staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from typing import Annotated

def dependency1():
    print("global dependency 1")

def dependency2():
    print("global dependency 2")

app = FastAPI(dependencies=[Depends(dependency1), Depends(dependency2)])

static_path = os.path.join(os.path.dirname(__file__), 'static/')
templates_path = os.path.join(os.path.dirname(__file__), 'templates/')

app.mount('/static', StaticFiles(directory=static_path), 'static')
templates = Jinja2Templates(directory=templates_path)

#app.add_middleware(HTTPErrorHandler)



#def common_params(start_date: str, end_date:str):
#    return { "start_date": start_date, "end_date": end_date }

#CommonDep = Annotated[dict,  Depends(common_params)]

class CommonDep:
    def __init__(self, start_date: str, end_date:str) -> None:
        self.start_date = start_date
        self.end_date = end_date

@app.get('/users')
def get_users(commons: CommonDep = Depends(CommonDep)):
    return f"users created between {commons.start_date} and {commons.end_date}"

@app.get('/customers')
def get_customers(commons: CommonDep = Depends(CommonDep)):
    return f"customers created between{commons.start_date} and {commons.end_date}"




@app.middleware('http')
#asyn ES PARA ESCRIBIR CODIGO ASINCRONO OSEA QUE NO VA LINEA POR LINEA, SI NO QUE ESTA LA EJECUTA EN SEGUNDO PLANO MIENTRAS LAS DEMAS ESPERAN
async def http_error_handler(request:Request, call_next) -> Response | JSONResponse:
    print('middleware is running')
    return await call_next(request)

      
@app.get('/', tags=['homee'])
def home(request: Request):
    return templates.TemplateResponse('index.html', {'request': request, 'mensaje': 'Welcome'})

app.include_router(prefix='/movies', router=movie_router)


