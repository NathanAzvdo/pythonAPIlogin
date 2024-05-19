from fastapi import APIRouter, Depends, HTTPException, FastAPI
from passlib.context import CryptContext
from app.models.UserModel import DB_user
from app.schemas.UserSchema import UserSchema
from app.database import SessionLocal, engine
from sqlalchemy.orm import Session, declarative_base
from typing import Annotated, List
import re

Base = declarative_base()
Base.metadata.create_all(bind=engine)


router = APIRouter()

def get_session() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

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
def createUser(user_data: UserSchema, db: Session = Depends(get_session)):
    errors = validate_entries(db, user_data)
    if errors:
        raise HTTPException(status_code=400, detail=errors)
    
    hashed_password = generate_hash(user_data.password)
    new_user = DB_user(name=user_data.name, email=user_data.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {'message': 'User saved!', 'user': new_user}

def validate_email_exists(db: Session, email: str) -> List[str]:
    user_email = db.query(DB_user).filter(DB_user.email == email).first()
    return ['Email already registered'] if user_email else []

def validate_email_format(email: str) -> List[str]:
    regex_email = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    return ["Invalid email address"] if not regex_email.match(email) else []

def validate_name(name: str) -> List[str]:
    if not name:
        return ["Name cannot be empty"]
    elif len(name) < 4:
        return ["The name must contain at least 4 characters"]
    return []

def validate_password(password: str) -> List[str]:
    errors = []
    if len(password) < 8:
        errors.append("The password must have at least 8 characters.")
    if not any(char.isupper() for char in password):
        errors.append('The password must contain at least one uppercase letter.')
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append('The password must contain at least one special character.')
    return errors

def validate_entries(db: Session, user_data: UserSchema) -> List[str]:
    errors = []
    errors.extend(validate_email_exists(db, user_data.email))
    errors.extend(validate_email_format(user_data.email))
    errors.extend(validate_name(user_data.name))
    errors.extend(validate_password(user_data.password))
    return errors

    
def generate_hash(password: str) -> str:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)
