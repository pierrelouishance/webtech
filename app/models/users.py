from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

class User(Base):
    __tablename__ = "users"

    id              = mapped_column(Integer, primary_key=True)
    email           = mapped_column(String(50), nullable=False, unique=True)
    nom             = mapped_column(String(50), nullable=False)
    prenom          = mapped_column(String(50), nullable=False)
    password        = mapped_column(String(50), nullable=False)
    confirm_password = mapped_column(String(50), nullable=False)
    role        = mapped_column(String(50), nullable=False)

    books = relationship("Book", back_populates="owner")