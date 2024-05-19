from sqlalchemy import select
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

from app.database import SessionLocal, engine


Base = declarative_base()


class DB_user(Base):
    __tablename__ = "user"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    
    
    
    
session = SessionLocal()
Base.metadata.create_all(bind=engine)



    