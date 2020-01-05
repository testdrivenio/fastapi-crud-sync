from fastapi import FastAPI

from app.db import engine
from app.api import ping, notes
from app.api.models import Base


Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(ping.router)
app.include_router(notes.router, prefix="/notes", tags=["notes"])
