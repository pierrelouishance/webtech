# Définition des types forward-referenced
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.users import User
    from app.schemas.notes import Note
