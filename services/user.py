import jwt

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database.database import get_db
from settings.settings import settings

from schemas.user import UserDTO, UserUpdateDTO
from models.user import User


reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/sign-in"
)


async def get_current_user(token: str = Depends(reuseable_oauth), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user = db.query(User).get(payload["user_id"])
    except:
        raise HTTPException(detail="Invalid User", status_code=401)

    return UserDTO.from_orm(user)


def update(data: UserUpdateDTO, db: Session):
    user = db.query(User).get(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found!")
    user.email = data.name
    db.commit()
    db.refresh(user)
    return user
