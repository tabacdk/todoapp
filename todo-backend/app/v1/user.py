from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.user import UserCreate, UserRead
from app.services import user as user_service

router = APIRouter()

@router.post("/", response_model=UserRead)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await user_service.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return await user_service.create_user(db, user)

@router.get("/{username}", response_model=UserRead)
async def get_user(username: str, db: AsyncSession = Depends(get_db)):
    db_user = await user_service.get_user_by_username(db, username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
