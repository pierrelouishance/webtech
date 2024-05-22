from pydantic import BaseModel


class NoteSchema (BaseModel) :
    def __getitem__(self, key):

        return getattr(self, key)
    id: str
    text :str
    categorie : str


