from pathlib import Path
from fastapi import FastAPI
from sqlalchemy.orm import Session, declarative_base
from app.routes import users
from app.database import SessionLocal, engine


app = FastAPI()

app.include_router(users.router)

PROJECT_ROOT = Path(__file__).parent.parent