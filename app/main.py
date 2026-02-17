from fastapi import FastAPI, HTTPException

from app.db import init_db
from app.schemas import NoteCreate
from app import crud


app = FastAPI(title="Notes API v2")

init_db()


@app.post("/notes", status_code=201)
def create_note(note: NoteCreate):
    return crud.create_note(title=note.title, content=note.content)


@app.get("/notes")
def get_notes():
    return crud.get_notes()


@app.get("/notes/{note_id}")
def get_note(note_id: int):
    note = crud.get_note(note_id=note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    ok = crud.delete_note(note_id=note_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Deleted"}
