from sqlalchemy.orm import Session

from app.api.models import Note, NoteSchema


def post(db_session: Session, payload: NoteSchema):
    note = Note(title=payload.title, description=payload.description)
    db_session.add(note)
    db_session.commit()
    db_session.refresh(note)
    return note


def get(db_session: Session, id: int):
    return db_session.query(Note).filter(Note.id == id).first()


def get_all(db_session: Session):
    return db_session.query(Note).all()


def put(db_session: Session, note: Note, title: str, description: str):
    note.title = title
    note.description = description
    db_session.commit()
    return note


def delete(db_session: Session, id: int):
    note = db_session.query(Note).filter(Note.id == id).first()
    db_session.delete(note)
    db_session.commit()
    return note
