from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import relationship, mapped_column
from app.database.database import Base

class UserNote(Base):
    __tablename__ = "user_notes"

    user_id = mapped_column(String, ForeignKey('users.id'), primary_key=True)
    note_id = mapped_column(String, ForeignKey('notes.id'), primary_key=True)

    user = relationship("User", back_populates="shared_notes")
    note = relationship("Note", back_populates="shared_with")
