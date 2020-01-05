from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path

from app.db import SessionLocal
from app.api import crud
from app.api.models import NoteDB, NoteSchema


router = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.post("/", response_model=NoteDB, status_code=201)
def create_note(*, db: Session = Depends(get_db), payload: NoteSchema):
    note = crud.post(db_session=db, payload=payload)
    return note


@router.get("/{id}/", response_model=NoteDB)
def read_note(
    *, db: Session = Depends(get_db), id: int = Path(..., gt=0),
):
    note = crud.get(db_session=db, id=id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.get("/", response_model=List[NoteDB])
def read_all_notes(db: Session = Depends(get_db)):
    return crud.get_all(db_session=db)


@router.put("/{id}/", response_model=NoteDB)
def update_note(
    *, db: Session = Depends(get_db), id: int = Path(..., gt=0), payload: NoteSchema
):
    note = crud.get(db_session=db, id=id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    note = crud.put(
        db_session=db, note=note, title=payload.title, description=payload.description
    )
    return note


@router.delete("/{id}/", response_model=NoteDB)
def delete_note(
    *, db: Session = Depends(get_db), id: int = Path(..., gt=0),
):
    note = crud.get(db_session=db, id=id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    note = crud.delete(db_session=db, id=id)
    return note
