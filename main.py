from fastapi import FastAPI

from routers import assistance, category, auth, user


app = FastAPI()


app.include_router(assistance.router)
app.include_router(category.router)
app.include_router(auth.router)
app.include_router(user.router)
