from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Notes API", description="A simple API to manage notes", version="1.0.0")

notes: list[dict] = []

class CreateNote(BaseModel):
    title: str
    content: str


@app.post("/notes", status_code=201)
def create_note(note: CreateNote):
    note_id = len(notes) + 1

    new_note = {
        "id": note_id, 
        "title": note.title, 
        "content": note.content
        }
    
    notes.append(new_note)

    return new_note


@app.get("/notes")
def get_all_notes():
    return notes


@app.get("/notes/(note_id)")
def get_note_by_id(note_id: int):
    for note in notes:
        if note["id"] == note_id:
            return note
    
    raise HTTPException(status_code=404, detail="Note not found")


@app.delete("/notes/{note_id}", status_code=204)
def delete_note_by_id(note_id: int):
    for note in notes:
        if note["id"] == note.id:
            notes.remove(note)
            return {"message": "Note deleted successfully"}
        
    raise HTTPException(status_code=404, detail="Note not found")


