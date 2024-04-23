from sqlalchemy import String, ForeignKey, Float
from sqlalchemy.orm import relationship, mapped_column, Mapped
from typing import Optional 

from app.database import Base

class Book(Base):
    __tablename__ = "books"

    id      = mapped_column(String, primary_key=True)
    name     = mapped_column(String(50), nullable=False, unique=True)
    auteur  = mapped_column(String(50), nullable=False)
    editeur : Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    prix    = mapped_column(Float, nullable=False)
    is_sale = mapped_column(String, nullable=False)
    
    owner_id =  mapped_column(String, ForeignKey('users.id'))

    owner = relationship("User", back_populates="books")