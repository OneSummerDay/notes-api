from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3


app = FastAPI(title="Notes API", description="A simple API to manage notes", version="2.0.0")

conn = sqlite3.connect("notes.db", check_same_thread=False)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL
)
""")

conn.commit()

class CreateNote(BaseModel):
    title: str
    content: str


@app.post("/notes", status_code=201)
def create_note(note: CreateNote):
    cursor.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (note.title, note.content))
    conn.commit()
    note_id = cursor.lastrowid
    return {
        "id": note_id,
        "title": note.title,
        "content": note.content
    }


@app.get("/notes")
def get_all_notes():
    cursor.execute("SELECT id, title, content FROM notes")
    rows = cursor.fetchall()
    notes = []
    for row in rows:
        notes.append({
            "id": row[0],
            "title": row[1],
            "content": row[2]
        })

    return notes


@app.get("/notes/{note_id}")
def get_note_by_id(note_id: int):
    cursor.execute("SELECT id, title, content FROM notes WHERE id = ?", (note_id))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return {
        "id": row[0],
        "title": row[1],
        "content": row[2]
    }


@app.delete("/notes/{note_id}", status_code=204)
def delete_note_by_id(note_id: int):
    cursor.execute("DELETE FROM notes WHERE id = ?", (note_id))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Note not found")
    conn.commit()

    return {"message": "Note deleted successfully"}


