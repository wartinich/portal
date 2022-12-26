from sqlalchemy import Boolean, Column, Integer, String, ForeignKey

from database.database import Base


class Assistance(Base):
    __tablename__ = "assistance"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    payment_url = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    is_active = Column(Boolean, default=True)
