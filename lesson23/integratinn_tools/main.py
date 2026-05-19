from pydoc import describe
from random import sample

from fastapi import FastAPI
from streamlit import title

from models import Developer, Project

app = FastAPI()

@app.post("/developer/")
def create_developers(developer: Developer):
    return {"message": "Developer created successfully", "developer": developer}

@app.get("/projects/")
def get_projects():

    sample_project = Project(
        title="Sample Project",
        description="This is a sample project",
        languages=["Python","JavaScript"],
        lead_developer=Developer(name="Dion Konjuhi", experience=5)
    )
    return {"projects": [sample_project]}
