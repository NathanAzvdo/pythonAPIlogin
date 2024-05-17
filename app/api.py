from starlette.staticfiles import StaticFiles
from pathlib import Path
from fastapi import FastAPI
from sqlalchemy.orm import Session, declarative_base
from app.routes import users
from app.database import SessionLocal, engine


app = FastAPI()


app.include_router(users.router)

PROJECT_ROOT = Path(__file__).parent.parent
print(PROJECT_ROOT)
app.mount('/', StaticFiles(directory=PROJECT_ROOT / 'static', html=True))