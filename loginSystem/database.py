import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

load_dotenv('/home/nathan/Documentos/apirestPy/loginSystem/.env')
db_url = os.environ.get('db_url')
print(db_url)
engine = create_engine(
    db_url,
    connect_args={'check_same_thread': False},
)
SessionLocal = sessionmaker(bind=engine)
