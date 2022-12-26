from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db

from services.user import get_current_user, update
from schemas.user import UserDTO, UserUpdateDTO


router = APIRouter(tags=["user"])


@router.get("/user/me", response_model=UserDTO)
async def user_profile(user: UserDTO = Depends(get_current_user)):
    return user


@router.patch("/user/me", response_model=UserUpdateDTO)
async def user_update(user: UserUpdateDTO, db: Session = Depends(get_db)):
    result = update(user, db)
    return result
