from app.database import database
from app.schemas.users import UserSchema


def get_user_by_username(username: str):
    for user in database['users']:
        if user['username'] == username:
            return UserSchema.model_validate(user)
    return None


def get_user_by_id(id: str):
    for user in database['users']:
        if user['id'] == id:
            return UserSchema.model_validate(user)
    return None

def create_user(new_user: UserSchema) -> UserSchema:

    user_dict = new_user.dict()  # Conversion de l'objet Pydantic en dictionnaire
    database["users"].append(user_dict)
    return new_user