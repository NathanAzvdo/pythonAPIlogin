from fastapi import APIRouter, Depends, HTTPException, FastAPI
from passlib.context import CryptContext
from app.models.UserModel import DB_user
from app.schemas.UserSchema import UserSchema
from app.database import SessionLocal, engine
from sqlalchemy.orm import Session, declarative_base
from typing import Annotated

Base = declarative_base()
Base.metadata.create_all(bind=engine)


router = APIRouter()

def get_session() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def generate_hash(password: str) -> str:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)

@router.get('/ping')
def ping() -> str:
    return 'pong'

@router.get('/getUser/{id}')
def getUserbyId(id:int, db: Annotated[Session, Depends(get_session)]):
    user = db.get(DB_user, id)
    if user is None:
        raise HTTPException(status_code=404, detail='Client not found!')
    return user

@router.post('/createUser')
def createUser(user_data: UserSchema, db: Annotated[Session, Depends(get_session)]):
    if validateUserExists(db, user_data.email):
        raise HTTPException(status_code=409, detail='Email already exists')
    hashed_password = generate_hash(user_data.password)
    new_user = DB_user(name=user_data.name, email=user_data.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return 'User saved!', new_user

def validateUserExists(db, email):
    user_email = db.query(DB_user).filter(DB_user.email == email).first()
    return True if user_email else False

