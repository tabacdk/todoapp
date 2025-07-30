from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.todo import TodoCreate, TodoRead
from app.services import todo as todo_service

router = APIRouter()

@router.post("/", response_model=TodoRead)
async def create_todo(todo: TodoCreate, db: AsyncSession = Depends(get_db)):
    return await todo_service.create_todo(db, todo)

@router.get("/{todo_id}", response_model=TodoRead)
async def read_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    todo = await todo_service.get_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.get("/", response_model=list[TodoRead])
async def read_all_todos(db: AsyncSession = Depends(get_db)):
    return await todo_service.get_all_todos(db)
