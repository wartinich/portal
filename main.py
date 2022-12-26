from fastapi import FastAPI

from database.database import Base, engine
from routers import assistance, category, auth, user


app = FastAPI()


Base.metadata.create_all(bind=engine)


app.include_router(assistance.router)
app.include_router(category.router)
app.include_router(auth.router)
app.include_router(user.router)
