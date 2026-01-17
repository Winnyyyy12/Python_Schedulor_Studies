# app/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy impor  t SQLAlchemyJobStore
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger
from datetime import datetime
from app.websocket_mgr import ws_manager
from app.db import engine, SessionLocal
from app import crud
import traceback
import asyncio
import os
from app.db import SYNC_DB

jobstores = {
    "default": SQLAlchemyJobStore(url=SYNC_DB)
}

scheduler = AsyncIOScheduler(jobstores=jobstores)

async def _make_db_session():
    return SessionLocal()

async def job_runner(job_id: str, payload: dict):
    db = await _make_db_session()
    try:
        # Example: do any work here — for demo we just log
        message = f"Job {job_id} executed with payload: {payload}"
        log = crud.create_log(db, job_id=job_id, status="success", message=message)

        # Broadcast to websocket clients in realtime
        asyncio.create_task(ws_manager.broadcast({
            "type": "job_run",
            "job_id": job_id,
            "run_time": log.run_time.isoformat(),
            "status": log.status,
            "message": log.message
        }))
    except Exception as e:
        crud.create_log(db, job_id=job_id, status="failure", message=str(e))
        asyncio.create_task(ws_manager.broadcast({
            "type": "job_run",
            "job_id": job_id,
            "run_time": datetime.now().isoformat(),
            "status": "failure",
            "message": str(e)
        }))
    finally:
        db.close()

async def init_scheduler():
    if not scheduler.running:
        scheduler.start()

async def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)

# helpers to add jobs
async def add_cron_job(job_id: str, cron_args: dict, payload: dict):
    trigger = CronTrigger(**cron_args)
    scheduler.add_job(job_runner, trigger=trigger, id=job_id, args=[job_id, payload], replace_existing=True)
    return scheduler.get_job(job_id)

async def add_interval_job(job_id: str, seconds=None, minutes=None, hours=None, payload=None):
    trigger = IntervalTrigger(seconds=seconds or 0, minutes=minutes or 0, hours=hours or 0)
    scheduler.add_job(job_runner, trigger=trigger, id=job_id, args=[job_id, payload or {}], replace_existing=True)
    return scheduler.get_job(job_id)

async def add_date_job(job_id: str, run_date: datetime, payload=None):
    trigger = DateTrigger(run_date=run_date)
    scheduler.add_job(job_runner, trigger=trigger, id=job_id, args=[job_id, payload or {}], replace_existing=True)
    return scheduler.get_job(job_id)
