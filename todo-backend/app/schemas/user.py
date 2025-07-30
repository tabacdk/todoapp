from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str  # plaintext ved oprettelse

class UserRead(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True
