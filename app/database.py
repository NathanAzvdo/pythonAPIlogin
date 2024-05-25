import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from pathlib import Path

path = Path(__file__).parent.parent
load_dotenv(f'{path}/config/.env')

db_url = os.environ.get('db_url')
engine = create_engine(
    db_url,
    connect_args={'check_same_thread': False},
)

SessionLocal = sessionmaker(bind=engine)
