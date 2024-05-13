from fastapi import APIRouter, Depends, HTTPException, FastAPI
from sqlalchemy.orm import Session
from loginSystem.schemas import UserSchema
from loginSystem.models import DB_user
from loginSystem.database import SessionLocal
from passlib.context import CryptContext

router = APIRouter()

def get_session() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()



def generate_hash(password: str) -> str:
    return pwd_context.hash(password)
        
@router.get('/getUs/{email}')
def getUS(email: str, db: Session = Depends(SessionLocal)):
    user = db.query(DB_user).filter(DB_user.email == email).first()
    if user is None:
        raise HTTPException(status_code=404, detail=f"No user found with this email")
    return user

@router.post('/createUS')
def createUs(user_data: UserSchema, db: Session = Depends(SessionLocal)):
    print(user_data)
    try:
        user = db.query(DB_user).filter(DB_user.email == user_data.email).first()
        if user:
            raise HTTPException(status_code=400, detail="User already exists")
        new_user = DB_user(**user_data.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        return e