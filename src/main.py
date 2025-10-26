from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse,RedirectResponse, FileResponse
from pydantic import BaseModel, Field, field_validator, ValidationError

from typing import Optional, List
import datetime
from src.routers.movie_router import movie_router

app = FastAPI()


@app.get('/', tags=['homee'])
def homee():
    return PlainTextResponse(content='Home', status_code=200)


app.include_router(prefix='/movies', router=movie_router)


