import uuid
from sqlalchemy.orm import Session
from app.models.users import User
from app.database import Session
from werkzeug.security import generate_password_hash
from app.models.books import Book

def init_db():
    db = Session()

    admin = db.query(User).filter(User.email == "admin").first()
    if not admin:
        admin = User(
            email="admin",
            nom="Admin",
            prenom="Admin",
            password=generate_password_hash("admin"),
            confirm_password=generate_password_hash("admin"),  
            role="admin"
        )
        db.add(admin)

    user1 = db.query(User).filter(User.email == "user1@example.com").first()
    if not user1:
        user1 = User(
            email="user1@example.com",
            nom="User",
            prenom="One",
            password=generate_password_hash("password"),
            confirm_password=generate_password_hash("password"),
            role="client"
        )
        db.add(user1)
    book1 = db.query(Book).join(User).filter(Book.nom == "Book One", User.email == "admin").first()
    if not book1 : 
        new = admin.id #recuperer l'id de l'administarteur 
        book1 = Book(
            nom="Book One",
            auteur="Author One",
            editeur="Author One",
            prix=9.99,
            is_sale="à vendre",
            owner_id=new,
        )
        db.add(book1)
    book2 = db.query(Book).join(User).filter(Book.nom == "Book Two", User.email == "user1@example.com").first()
    if not book2 : 
        new = user1.id  
        book2 = Book(
            nom="Book Two",
            auteur="Author Two",
            editeur="Author Two",
            prix=19.99,
            is_sale="à vendre",
            owner_id=new,
        )
        db.add(book2)
    
    db.commit()
