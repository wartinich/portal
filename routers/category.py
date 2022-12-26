from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database.database import get_db

from schemas.category import CategoryDTO
from services.category import create, get_list, update


router = APIRouter(tags=["categories"])


@router.post("/categories", response_model=CategoryDTO)
async def create_category(body: CategoryDTO, db: Session = Depends(get_db)):
    result = create(body, db)
    return result


@router.get("/categories", response_model=List[CategoryDTO])
async def category_list(db: Session = Depends(get_db)):
    result = get_list(db)
    return result


@router.patch("/categories/{id}", response_model=CategoryDTO)
async def category_update(id: int, body: CategoryDTO, db: Session = Depends(get_db)):
    result = update(id, body, db)
    return result
