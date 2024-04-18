
from typing import Optional
from pydantic import BaseModel, Field


class BookSchema(BaseModel):

    def __getitem__(self, key):
        return getattr(self, key)

    id: str
    name: str = Field(min_length=3, max_length=50)
    auteur: str = Field(min_length=3, max_length=50)
    editeur: Optional[str] = Field(min_length=3, max_length=50)
    prix : float
    is_sale : str
    owner_id : str 