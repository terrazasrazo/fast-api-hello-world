# Python
from importlib.resources import path
from re import S
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel, Field
from pydantic import EmailStr, HttpUrl

# FastAPI
from fastapi import FastAPI, Body, Path, Query, status

app = FastAPI()

# Models

class HairColor(Enum):
    white = 'white'
    brown = 'brown'
    black = 'black'
    blonde = 'blonde'
    red = 'red'

class PersonBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    age: int = Field(..., gt=0, le=115)
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)  

class Person(PersonBase):
    password: str = Field(..., min_length=8)
    """"
    class Config:
        schema_extra = {
            "example": {
                "first_name": "Omar",
                "last_name": "Terrazas",
                "age": 37,
                "hair_color": "black",
                "is_married": True
            }
        }
    """

class PersonOut(PersonBase):
    pass

class Location(BaseModel):
    email: EmailStr = Field(..., example="terrazas.omar@gmail.com")
    webpage: Optional[HttpUrl] = Field(example="https://twitter.com/terracing")
    country: str = Field(..., example="México")


@app.get(path="/", status_code=status.HTTP_200_OK)
def home():
    return {"Hello": "world"}

# Request and Response Body
@app.post(path="/person/new", response_model=PersonOut, status_code=status.HTTP_201_CREATED)
def create_person(person: Person = Body(...)):
    return person

# Validaciones: Query Parameters
@app.get(path="/person/detail", status_code=status.HTTP_200_OK)
def show_person(
    name: Optional[str] = Query(None, min_length=1, max_length=50, example="Omar Terrazas"),
    age: int = Query(...)
):
    return {name: age}

# Validaciones: Path Parameters
@app.get(path="/person/detail/{person_id}", status_code=status.HTTP_200_OK)
def show_person(
    person_id: int = Path(..., gt=0, title="Person Id", example=123, description="Identificador to person into database")
):
    return {person_id: "It's exists!"}

# Validaciones: Request Body
@app.put(path="/person/{person_id}", status_code=status.HTTP_202_ACCEPTED)
def update_person(
    person_id: int = Path(..., gt=0, title="Person Id", example=123, description="Identificador to person into database"),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results

