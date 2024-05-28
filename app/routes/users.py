from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.auth.auth import get_current_user
from app.models.UserModel import DB_user
from app.controllers.user_controller import (
    get_session,
    create_user,
    UserSchema,
    UserLoginSchema,
    login_user
)

router = APIRouter()

@router.post('/createUser')
def route_create_user(user_data: UserSchema, db: Session = Depends(get_session)):
    return create_user(user_data, db)

@router.post('/login')
def route_login(user_data: UserLoginSchema, db: Session = Depends(get_session)):
    return f'Token: {login_user(user_data, db)}'
    
@router.get("/protected")
def protected_route(current_user: DB_user = Depends(get_current_user)):
    return {"message": "This is a protected route", "user": current_user.name}