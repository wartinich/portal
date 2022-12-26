from pydantic import BaseConfig


class Setting(BaseConfig):
    DATABASE_URL: str = "sqlite:///./portal.db"
    JWT_SECRET: str = "secret"
    JWT_ALGORITHM: str = "HS256"


settings = Setting()
