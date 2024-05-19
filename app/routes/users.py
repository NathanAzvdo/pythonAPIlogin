from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.controllers.user_controller import (
    get_session,
    create_user,
    UserSchema
)

router = APIRouter()

@router.post('/createUser')
def route_create_user(user_data: UserSchema, db: Session = Depends(get_session)):
    return create_user(user_data, db)
