# app/routers/logs.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app import crud
from app import schemas
from app.db import get_db

router = APIRouter(prefix="/logs", tags=["logs"])

@router.get("", response_model=List[schemas.JobLogOut])
def get_logs(limit: int = 50, db: Session = Depends(get_db)):
    return crud.list_logs(db, limit=limit)
