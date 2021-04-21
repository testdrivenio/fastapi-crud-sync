from fastapi import FastAPI

from app.api import ping, notes
from app.api.models import Base
from app.db import engine


Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(ping.router)
app.include_router(notes.router, prefix="/notes", tags=["notes"])
