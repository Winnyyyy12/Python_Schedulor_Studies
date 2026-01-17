# app/models.py
from sqlalchemy import Column, Integer, String, DateTime, Text, func
from app.db import Base
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class JobLog(Base):  #log table model
    __tablename__ = "job_logs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String(100), index=True)
    run_time = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(50))
    message = Column(Text, nullable=True)