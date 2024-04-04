
from pydantic import BaseModel, Field


class User(BaseModel):
    email: str
    password: str
    first_name: str = Field(min_length=3, max_length=50)
    last_name: str = Field(min_length=3, max_length=50)
    group: str = "client"  # Par défaut, l'utilisateur est un client