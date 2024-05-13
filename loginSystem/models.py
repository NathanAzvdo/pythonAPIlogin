from sqlalchemy import select
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

from loginSystem.database import SessionLocal, engine

Base = declarative_base()

class DB_user(Base):
    __tablename__ = "user"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(unique=True)
    Eadmin: Mapped[int] = mapped_column(default=0)
    
    
    
    
session = SessionLocal()


    