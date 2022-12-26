from sqlalchemy.orm import Session
from fastapi import HTTPException

from schemas.assistance import AssistanceDTO
from models.category import Category
from models.assistance import Assistance
from models.user import User


def create(data: AssistanceDTO, user, db: Session):
    category = db.query(Category).filter(Category.name == data.category).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found!")

    new_assistance = Assistance(
        name=data.name,
        payment_url=data.payment_url,
        category_id=category.id,
        user_id=user.id
    )

    db.add(new_assistance)
    db.commit()
    return data


def get_list(db: Session):
    assistance = db.query(Assistance).all()
    items = []

    for item in assistance:
        category = db.query(Category).get(item.category_id)
        user = db.query(User).get(item.user_id)

        data = {
            "name": item.name,
            "payment_url": item.payment_url,
            "category": category.name,
            "user": {
                "email": user.email
            }
        }
        items.append(data)

    return items


def get_by_id(id: int, db: Session):
    assistance = db.query(Assistance).get(id)
    if not assistance:
        raise HTTPException(status_code=404, detail="Assistance not found!")

    category = db.query(Category).get(assistance.category_id)
    user = db.query(User).get(assistance.user_id)

    return {
        "name": assistance.name,
        "payment_url": assistance.payment_url,
        "category": category.name,
        "user": {
            "email": user.email
        }
    }


def update(id: int, data: AssistanceDTO, user, db: Session):
    assistance = db.query(Assistance).get(id)
    category = db.query(Category).filter(Category.name == data.category).first()

    if user.id != assistance.user_id:
        raise HTTPException(status_code=404, detail="Invalid user")

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    if not assistance:
        raise HTTPException(status_code=404, detail="Assistance not found!")

    assistance.name = data.name
    assistance.payment_url = data.payment_url
    assistance.categort_id = category.name
    db.commit()
    db.refresh(assistance)

    return {
        "name": assistance.name,
        "payment_url": assistance.payment_url,
        "category": category.name
    }
