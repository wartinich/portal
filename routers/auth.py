from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from schemas.user import UserCreateDTO
from services.auth import create_user, check_user, signJWT, JWTBearerRefresh


router = APIRouter(tags=["auth"])


@router.post("/sign-up")
async def sign_up(body: UserCreateDTO, db: Session = Depends(get_db)):
    result = create_user(body, db)
    return signJWT(result.id)


@router.post("/sign-in")
async def sign_in(body: UserCreateDTO, db: Session = Depends(get_db)):
    if data := check_user(body, db):
        return signJWT(data.id)
    return HTTPException(detail="Wrong login details!", status_code=200)


@router.get('/refresh/', dependencies=[Depends(JWTBearerRefresh())])
async def refresh(token: int = Depends(JWTBearerRefresh()), db: Session = Depends(get_db)):
    return signJWT(token["user_id"])
