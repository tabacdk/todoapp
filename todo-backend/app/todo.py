from fastapi import APIRouter

router = APIRouter()

@router.get("/{todo_id}")
def get_todo(todo_id: int):
    return {"todo_id": todo_id}

@router.post("/new")
def create_todo():
    return {"message": "new todo created (stub)"}
