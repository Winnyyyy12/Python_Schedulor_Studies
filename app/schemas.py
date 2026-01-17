# app/schemas.py
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class JobCreate(BaseModel):
    id:str
    cron: str

class JobCreateCron(BaseModel):
    id: Optional[str]
    cron: Dict[str, Any]  # e.g., {"minute":"*/5"} or {"hour":"6","minute":"30"}
    args: Optional[Dict[str, Any]] = {}

class JobCreateInterval(BaseModel):
    id: Optional[str]
    seconds: Optional[int] = None
    minutes: Optional[int] = None
    hours: Optional[int] = None
    args: Optional[Dict[str, Any]] = {}

class JobCreateDate(BaseModel):
    id: Optional[str]
    run_date: datetime
    args: Optional[Dict[str, Any]] = {}

class JobInfo(BaseModel):
    id: str
    next_run_time: Optional[datetime]
    trigger: str

class JobLogOut(BaseModel):
    id: int
    job_id: str
    run_time: datetime
    status: str
    message: Optional[str]
