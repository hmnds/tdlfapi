from fastapi import FastAPI
from app.db.database import Base, engine
from dotenv import load_dotenv
from app.models import *
from app.routes import api_router

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api_router)