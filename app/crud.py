from app.db import cursor, conn

# Create
def create_note(title: str, content: str) -> dict:
    cursor.execute(
        "INSERT INTO notes (title, content) VALUES (?, ?)",
        (title, content),
    )
    conn.commit()

    note_id = cursor.lastrowid

    return {"id": note_id, "title": title, "content": content}


# Read all
def get_notes() -> list[dict]:
    cursor.execute("SELECT id, title, content FROM notes")
    rows = cursor.fetchall()

    notes: list[dict] = []
    for row in rows:
        notes.append({"id": row[0], "title": row[1], "content": row[2]})

    return notes


# Read one
def get_note(note_id: int) -> dict | None:
    cursor.execute(
        "SELECT id, title, content FROM notes WHERE id = ?",
        (note_id,),
    )
    row = cursor.fetchone()

    if row is None:
        return None

    return {"id": row[0], "title": row[1], "content": row[2]}


# DeleteE
def delete_note(note_id: int) -> bool:
    cursor.execute(
        "DELETE FROM notes WHERE id = ?",
        (note_id,),
    )

  
    if cursor.rowcount == 0:
        return False

    conn.commit()
    return True
