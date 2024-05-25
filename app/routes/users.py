from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.controllers.user_controller import (
    get_session,
    create_user,
    UserSchema,
    login_user
)

router = APIRouter()

@router.post('/createUser')
def route_create_user(user_data: UserSchema, db: Session = Depends(get_session)):
    return create_user(user_data, db)

@router.post('/login')
def route_login(user_data: UserSchema, db: Session = Depends(get_session)):
    return f'Token: {login_user(user_data, db)}'
    
