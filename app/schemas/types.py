from pydantic import BaseModel

class NoteShareSchema(BaseModel):
    note_id: str
    user_id: str
