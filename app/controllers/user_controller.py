# app/controllers/user_controller.py
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.models.UserModel import DB_user
from app.schemas.UserSchema import UserSchema, UserLoginSchema
from app.schemas.Token import Token
from app.database import get_session
from pathlib import Path
from dotenv import load_dotenv
import os
import re
from datetime import datetime, timedelta
import jwt




path = Path(__file__).parent.parent
load_dotenv(f'{path}/config/.env')
SECRET_KEY = os.environ.get('KEY')
ALGORITHM = os.environ.get('alg')
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(user_data: UserSchema, db: Session = Depends(get_session)) -> dict:
    errors = validate_entries(db, user_data)
    if errors:
        raise HTTPException(status_code=400, detail=errors)
    
    return save_user(user_data, db)

def validate_entries(db: Session, user_data: UserSchema) -> list:
    errors = []
    errors.extend(validate_email_exists(db, user_data.email))
    errors.extend(validate_email_format(user_data.email))
    errors.extend(validate_name(user_data.name))
    errors.extend(validate_password(user_data.password))
    return errors

def save_user(user_data, db) -> dict:
    try:
        hashed_password = generate_hash(user_data.password)
        new_user = DB_user(name=user_data.name, email=user_data.email, password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {'message': 'User saved!', 'user': new_user}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error to save user, try again later") from e 

def validate_email_exists(db: Session, email: str) -> list:
    try:
        user_email = db.query(DB_user).filter(DB_user.email == email).first()
        return ['Email already registered'] if user_email else []
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error to validate email. try again later!") from e

def validate_email_format(email: str) -> list:
    regex_email = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    return ["Invalid email address"] if not regex_email.match(email) else []

def validate_name(name: str) -> list:
    if not name:
        return ["Name cannot be empty"]
    elif len(name) < 4:
        return ["The name must contain at least 4 characters"]
    return []

def validate_password(password: str) -> list:
    errors = []
    if len(password) < 8:
        errors.append("The password must have at least 8 characters.")
    if not any(char.isupper() for char in password):
        errors.append('The password must contain at least one uppercase letter.')
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append('The password must contain at least one special character.')
    return errors

def generate_hash(password: str) -> str:
    return pwd_context.hash(password)

def login_user(user_data: UserLoginSchema, db: Session = Depends(get_session)) -> Token:
    user = authenticate_user(user_data.email, user_data.password, db)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

def authenticate_user(email: str, password: str, db: Session) -> DB_user:
    user = db.query(DB_user).filter(DB_user.email == email).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Email/password incorrect")
    return user

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    register_token_to_env(encoded_jwt)
    return encoded_jwt

def register_token_to_env(jwt):
    os.environ['session_token']=jwt
    print(os.environ.get('session_token'))
        