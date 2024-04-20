from uuid import uuid4
from fastapi import HTTPException
from app.database import Session
from app.models.users import User 
from werkzeug.security import generate_password_hash

def get_db():
    return Session()

def get_all_users():
    with get_db() as db:
        return db.query(User).all()
    
def get_user_by_email(email: str):
    with get_db() as db:
        return db.query(User).filter(User.email == email).first()

def get_user_by_id(id: str):
    with get_db() as db:
        return db.query(User).filter(User.id == id).first()


def create_user(new_user: User):
    with get_db() as db:
        # Vérifiez si l'utilisateur existe déjà
        db_user = db.query(User).filter(User.email == new_user.email).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        # Hachez le mot de passe avant de l'enregistrer dans la base de données
        hashed_password = generate_password_hash(new_user.password)

        # Créez un nouvel objet utilisateur
        db_user = User(
            id = str(uuid4()),
            email=new_user.email,
            name=new_user.name,
            prenom=new_user.prenom,
            password=hashed_password,
            confirm_password = hashed_password,
            role=new_user.role
        )

        # Ajoutez l'utilisateur à la base de données et validez la transaction
        db.add(db_user)
        db.commit()

        # Rafraîchissez l'objet utilisateur pour obtenir toutes les colonnes, y compris l'ID
        db.refresh(db_user)

        return db_user
