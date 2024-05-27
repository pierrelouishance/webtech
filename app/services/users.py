from uuid import uuid4
from fastapi import HTTPException
from app.database.database import Session
from app.models.users import User 
from werkzeug.security import generate_password_hash,  check_password_hash

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
            password=hashed_password,
            confirm_password = hashed_password,
        )

        # Ajoutez l'utilisateur à la base de données et validez la transaction
        db.add(db_user)
        db.commit()

        # Rafraîchissez l'objet utilisateur pour obtenir toutes les colonnes, y compris l'ID
        db.refresh(db_user)

        return db_user
    

def update_user(updated_user: User):
    with get_db() as db:
        # Recherche l'utilisateur dans la base de données
        db_user = db.query(User).filter(User.id == updated_user.id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Met à jour les informations de l'utilisateur
        db_user.name = updated_user.name
        db_user.email = updated_user.email
        db_user.password = updated_user.password
        db_user.confirm_password = updated_user.password

        # Enregistre les modifications dans la base de données
        db.commit()

        return db_user