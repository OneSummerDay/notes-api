from pydantic import BaseModel


class CreateNote(BaseModel):
    title: str
    content: str