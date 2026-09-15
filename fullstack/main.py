from http.client import HTTPException

from fastapi import FastAPI
from typing import List

from keras.src.legacy.backend import update_add
from ollama import delete
from streamlit import status

import database
import models
from models import Movie, MovieCreate

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to api crud"}

@app.post("/movies/", response_model=Movie)
def creaate_movie(movie: MovieCreate):
    movie_id = database.create_movie(movie)
    return models.Movie(id=movie_id, **movie.dict())

@app.get("movies", response_model=List[Movie])
def read_movies():
    return database.read_movie()

@app.get("/movies/{movie_id}", respose_model=Movie)
def update_movie(movie_id: int, movie:MovieCreate):
    updated = database.update_movie(movie_id, movie)
    if not updated:
        raise HTTPException(status_code=404, detail="Movie not found")
    return models.Movie(id=movie_id, **movie.dict())

@app.delete("/movies/{movie_id}", response_model=dict)
def delete_movie(movie_id: int):
    deleted = database.delete_movie(movie_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"message": "Movie got deleted"}
