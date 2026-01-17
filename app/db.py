from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

ASYNC_DB = os.getenv("ASYNC_DATABASE_URL")
SYNC_DB = os.getenv("SYNC_DATABASE_URL")

engine = create_async_engine(ASYNC_DB, echo=True) #Async engine for FastAPI

SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base() #base for models

# Scheduler’s sync engine
sync_engine = create_engine(SYNC_DB, echo=True) #sync engine for scheduler

def get_db(): #generator for DB session in fastapi(dependency injection)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
