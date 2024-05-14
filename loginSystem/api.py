from starlette.staticfiles import StaticFiles
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, FastAPI
from sqlalchemy.orm import Session, declarative_base

from passlib.context import CryptContext

from loginSystem.models import DB_user
from loginSystem.schemas import UserSchema
from loginSystem.database import SessionLocal, engine

from typing import Annotated

app = FastAPI()
Base = declarative_base()

Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_hash(password: str) -> str:
    return pwd_context.hash(password)

def get_session() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


PROJECT_ROOT = Path(__file__).parent.parent

@app.get('/ping')
def ping() -> str:
    return 'pong'

@app.get('/getUser/{id}')
def getUser(id:int, db: Annotated[Session, Depends(get_session)]):
    user = db.get(DB_user, id)
    if user is None:
        raise HTTPException(status_code=404, detail=f'No client with id:{id}')
    return user

@app.post('/createUser')
def createUs(user_data: UserSchema, db: Annotated[Session, Depends(get_session)]):
    hashed_password = generate_hash(user_data.password)
    user = db.query(DB_user).filter(DB_user.email == user_data.email or DB_user.name == user_data.name).first()
    if user:
        raise HTTPException(status_code=400, detail="User already exists")
    new_user = DB_user(name=user_data.name, email=user_data.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return 'User saved!', new_user


app.mount('/', StaticFiles(directory=PROJECT_ROOT / 'static', html=True))