# Python
from typing import Optional
from unittest import result

# Pydantic
from pydantic import BaseModel

# FastAPI
from fastapi import FastAPI, Body, Path, Query

app = FastAPI()

# Models

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

class Location(BaseModel):
    city: str
    state: str
    country: str

@app.get("/")
def home():
    return {"Hello": "world"}

# Request and Response Body
@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person

# Validaciones: Query Parameters
@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(None, min_length=1, max_length=50),
    age: int = Query(...)
):
    return {name: age}

# Validaciones: Path Parameters
@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(..., gt=0, title="Person Id", description="Identificador to person into database")
):
    return {person_id: "It's exists!"}

# Validaciones: Request Body
@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(..., gt=0, title="Person Id", description="Identificador to person into database"),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results
