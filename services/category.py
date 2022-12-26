from fastapi import HTTPException
from sqlalchemy.orm import Session

from schemas.category import CategoryDTO
from models.category import Category


def create(data: CategoryDTO, db: Session) -> dict:
    new_category = Category(name=data.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return data


def get_list(db: Session) -> list:
    assistance = db.query(Category).all()
    return assistance


def update(id: int, data: CategoryDTO, db: Session) -> dict:
    category = db.query(Category).get(id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found!")
    category.name = data.name
    db.commit()
    db.refresh(category)
    return category
