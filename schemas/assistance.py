from pydantic import BaseModel


class AssistanceDTO(BaseModel):
    name: str
    payment_url: str
    category: str

    class Config:
        orm_mode = True
