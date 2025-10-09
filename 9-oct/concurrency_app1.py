from fastapi import FastAPI
import asyncio
import time

app = FastAPI()

@app.get("/sync-task")
def sync_task():
    time.sleep(10)  # blocking
    return {"message": "Sync task completed after 10 seconds"}

@app.get("/async-task")
async def async_task():
    await asyncio.sleep(10)  # non-blocking
    return {"message": "Async task completed after 10 seconds"}
