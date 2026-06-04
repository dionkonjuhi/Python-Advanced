from pydantic import BaseModel

class RecipeCreate():
    title: str
    director: str

class Movie(MovieCreate):
    id: int

