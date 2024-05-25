from sqlalchemy import String
from sqlalchemy.orm import relationship, mapped_column
from app.database.database import Base

class User(Base):
    __tablename__ = "users"

    id = mapped_column(String, primary_key=True)
    email = mapped_column(String(50), nullable=False, unique=True)
    name = mapped_column(String(50), nullable=False)
    password = mapped_column(String(50), nullable=False)
    confirm_password = mapped_column(String(50), nullable=False)
    
    notes = relationship("Note", back_populates="owner")
    shared_notes = relationship("UserNote", back_populates="user")
