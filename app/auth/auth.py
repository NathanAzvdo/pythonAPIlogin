# app/auth/auth.py
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.models.UserModel import DB_user
from app.database import get_session, load_dotenv
from dotenv import load_dotenv
from pathlib import Path
import os

path = Path(__file__).parent.parent
load_dotenv(f'{path}/config/.env')


SECRET_KEY = os.environ.get('KEY')
ALGORITHM = os.environ.get('alg')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(db: Session = Depends(get_session)) -> DB_user:

    token = os.environ.get('session_token')
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(DB_user).filter(DB_user.email == email).first()
    if user is None:
        raise credentials_exception
    
    return user
