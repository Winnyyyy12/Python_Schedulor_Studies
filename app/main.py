# app/main.py
from fastapi import FastAPI, WebSocket
from app.db import Base, engine
from app.scheduler import scheduler, init_scheduler, shutdown_scheduler
from sqlalchemy import text
from app.websocket_mgr import ws_manager
from app.routers import jobs, logs

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

app = FastAPI(title="Realtime Scheduler Backend")

# include routers
app.include_router(jobs.router)
app.include_router(logs.router)

# create DB tables + start scheduler on boot


@app.on_event("startup")
async def on_start():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    scheduler.start()


@app.on_event("shutdown")
async def on_shutdown():
    scheduler.shutdown_scheduler()


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws_manager.connect(ws) #accepts connection
    try:
        while True:
            data = await ws.receive_text()
            await ws.send_text("ack: " + data)
    except Exception:
        ws_manager.disconnect(ws)


