from pydantic import   BaseModel, EmailStr


class UserSchema(BaseModel):
    def __getitem__(self, key):
        return getattr(self, key)
    id: str
    prenom:str
    nom:str
    email: EmailStr
    password: str
    confirm_password: str
    role:str

