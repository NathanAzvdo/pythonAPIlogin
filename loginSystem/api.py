from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from pathlib import Path
from loginSystem.routes.user_routes import router
from loginSystem.database import SessionLocal, engine
from loginSystem.models import DB_user 

app = FastAPI()
app.include_router(router)

DB_user.metadata.create_all(bind=engine)
PROJECT_ROOT = Path(__file__).parent.parent

app.mount('/', StaticFiles(directory=PROJECT_ROOT / 'static', html=True))
