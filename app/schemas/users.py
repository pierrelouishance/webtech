from pydantic import   BaseModel


class UserSchema(BaseModel):
    def __getitem__(self, key):
        return getattr(self, key)
    id: str
    name:str
    email: str
    password: str
    confirm_password: str
