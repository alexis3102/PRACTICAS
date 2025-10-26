import datetime
from pydantic import BaseModel, Field, field_validator


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
