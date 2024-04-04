from pydantic import BaseModel


class UserSchema(BaseModel):
    id: str
    prenom:str
    nom:str
    username: str
    password: str
    role:str
