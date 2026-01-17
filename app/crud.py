# app/crud.py
from sqlalchemy.orm import Session
from app import models #import joblog model
from typing import List

def create_log(db: Session, job_id: str, status: str, message: str = None): #creates a new log entry
    log = models.JobLog(job_id=job_id, status=status, message=message) #intstantiates a joblog object
    db.add(log)
    db.commit() #saves to DB
    db.refresh(log)
    return log

def list_logs(db: Session, limit: int = 50):
    return db.query(models.JobLog).order_by(models.JobLog.run_time.desc()).limit(limit).all()
