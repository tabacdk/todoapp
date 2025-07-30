from pydantic import BaseModel

class TodoCreate(BaseModel):
    title: str
    description: str
    completed: bool = False
    user_id: int

class TodoRead(TodoCreate):
    id: int

    class Config:
        orm_mode = True
