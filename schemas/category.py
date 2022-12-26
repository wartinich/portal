from pydantic import BaseModel


class CategoryDTO(BaseModel):
    name: str

    class Config:
        orm_mode = True
