from fastapi import APIRouter

router = APIRouter()


@router.get("/ping")
def pong():
    return {"ping": "pong!"}
