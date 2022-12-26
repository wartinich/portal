from pydantic import BaseModel


class UserCreateDTO(BaseModel):
    email: str
    password: str


class UserDTO(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True


class UserUpdateDTO(BaseModel):
    email: str
