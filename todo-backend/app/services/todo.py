from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.todo import Todo
from app.schemas.todo import TodoCreate

async def create_todo(db: AsyncSession, todo_data: TodoCreate):
    todo = Todo(**todo_data.dict())
    db.add(todo)
    await db.commit()
    await db.refresh(todo)
    return todo

async def get_todo(db: AsyncSession, todo_id: int):
    stmt = select(Todo).where(Todo.id == todo_id)
    result = await db.execute(stmt)
    return result.scalars().first()

async def get_all_todos(db: AsyncSession):
    result = await db.execute(select(Todo))
    return result.scalars().all()
