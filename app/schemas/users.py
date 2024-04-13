from pydantic import BaseModel


class UserSchema(BaseModel):
    def __getitem__(self, key):
        return getattr(self, key)
    id: str
    prenom:str
    nom:str
    username: str
    password: str
    role:str
