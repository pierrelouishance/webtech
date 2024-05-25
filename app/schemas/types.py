# Définition des types forward-referenced
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.users import UserSchema
    from app.schemas.notes import NoteSchema
