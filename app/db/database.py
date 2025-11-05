from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL

if DATABASE_URL:
    engine = create_engine(DATABASE_URL, poolclass=QueuePool, pool_size=10, echo=True)
else:
    engine = None


if engine:
    SessionLocal = sessionmaker(bind=engine, autocommit=False)
else:
    SessionLocal = None

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()