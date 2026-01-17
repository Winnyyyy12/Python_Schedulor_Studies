# app/routers/jobs.py
from fastapi import APIRouter, HTTPException
from app import scheduler
from app import schemas
from typing import List
from datetime import datetime

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.post("/cron", response_model=schemas.JobInfo)
def create_cron_job(payload: schemas.JobCreateCron):
    job_id = payload.id or f"cron_{int(datetime.utcnow().timestamp())}"
    try:
        job = scheduler.add_cron_job(job_id, payload.cron, payload.args or {})
        return {
            "id": job.id,
            "next_run_time": job.next_run_time,
            "trigger": str(job.trigger)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/interval", response_model=schemas.JobInfo)
def create_interval_job(payload: schemas.JobCreateInterval):
    job_id = payload.id or f"interval_{int(datetime.utcnow().timestamp())}"
    try:
        job = scheduler.add_interval_job(job_id, seconds=payload.seconds, minutes=payload.minutes, hours=payload.hours, payload=payload.args or {})
        return {"id": job.id, "next_run_time": job.next_run_time, "trigger": str(job.trigger)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/date", response_model=schemas.JobInfo)
def create_date_job(payload: schemas.JobCreateDate):
    job_id = payload.id or f"date_{int(datetime.utcnow().timestamp())}"
    try:
        job = scheduler.add_date_job(job_id, run_date=payload.run_date, payload=payload.args or {})
        return {"id": job.id, "next_run_time": job.next_run_time, "trigger": str(job.trigger)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", response_model=List[schemas.JobInfo])
def list_jobs():
    jobs = scheduler.scheduler.get_jobs()
    result = []
    for j in jobs:
        result.append({"id": j.id, "next_run_time": j.next_run_time, "trigger": str(j.trigger)})
    return result

@router.delete("/{job_id}")
def delete_job(job_id: str):
    try:
        scheduler.scheduler.remove_job(job_id)
        return {"status": "deleted", "job_id": job_id}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
