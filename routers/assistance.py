from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from schemas.assistance import AssistanceDTO
from schemas.user import UserDTO

from services.assistance import create, get_list, get_by_id, update
from services.user import get_current_user


router = APIRouter(tags=["assistance"])


@router.post("/assistance")
async def add_assistance(
    body: AssistanceDTO, 
    user: UserDTO = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    result = create(body, user, db)
    return result


@router.get("/assistance")
async def assistance_list(db: Session = Depends(get_db)):
    result = get_list(db)
    return result


@router.get("/assistance/{id}")
async def assistance_detail(id: int, db: Session = Depends(get_db)):
    result = get_by_id(id, db)
    return result


@router.patch("/assistance/{id}")
async def assistance_update(
    id: int,
    body: AssistanceDTO,
    user: UserDTO = Depends(get_current_user), 
    db: Session = Depends(get_db), 
):
    result = update(id, body, user, db)
    return result
