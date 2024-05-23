from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship, mapped_column
from app.database.database import Base

class Note(Base):
    __tablename__ = "notes"

    id = mapped_column(String, primary_key=True)
    text = mapped_column(String(50), nullable=False)
    category = mapped_column(String, nullable=False)
    owner_id = mapped_column(String, ForeignKey('users.id'))

    owner = relationship("User", back_populates="notes")
    shared_with = relationship("UserNote", back_populates="note")
