from fastapi import APIRouter

router = APIRouter()

@router.get("/me")
def get_current_user():
    return {"user": "current (stub)"}

@router.get("/getuser/{username}")
def get_user_by_username(username: str):
    return {"user": username}
