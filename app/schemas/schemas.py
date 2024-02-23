
from pydantic import BaseModel, Field


class Book(BaseModel):
    id: str
    name: str = Field(min_length=3, max_length=50)
    auteur: str = Field(min_length=3, max_length=50)
    editeur: str = Field(min_length=3, max_length=50)

