from fastapi import FastAPI
from app.routers import contacts, users, auth
from app.db import engine
from app.models import Base

app = FastAPI()

# app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(auth.router)
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(contacts.router, prefix="/contacts", tags=["contacts"])

Base.metadata.create_all(bind=engine)