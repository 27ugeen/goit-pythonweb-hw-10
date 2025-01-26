from fastapi import FastAPI, Request
from app.routers import contacts, auth
from app.db import engine
from app.models import Base

from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from settings import settings

limiter = Limiter(key_func=get_remote_address)

app = FastAPI()

app.state.limiter = limiter

app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(contacts.router, prefix="/contacts", tags=["contacts"])

@app.get("/")
@limiter.limit(settings.RATE_LIMIT_GLOBAL)
async def root(request: Request):  # Додайте параметр request
    return {"message": "Welcome to the API"}

Base.metadata.create_all(bind=engine)