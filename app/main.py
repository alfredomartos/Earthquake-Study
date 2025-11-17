import asyncio
from fastapi import FastAPI

from app import crud
from .api.endpoints import router as earthquake_router
from .database import SessionLocal, engine
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Earthquake Data API")

async def periodic_ingestion():
    while True:
        print("BACKGROUND TASK: Starting periodic ingestion...")
        
        db = SessionLocal()
        try:
            crud.ingest_earthquake_data(db)
        except Exception as e:
            print(f"BACKGROUND TASK ERROR: {e}")
        finally:
            db.close()
            
        print("BACKGROUND TASK: Ingestion complete, sleeping for 10 seconds...")
        await asyncio.sleep(10)

@app.on_event("startup")
async def app_startup():
    print("STARTUP: Launching background ingestion task...")
    asyncio.create_task(periodic_ingestion())

app.include_router(earthquake_router)
@app.get("/")
def read_root():
    return {"message": "Welcome to the Earthquake Data API by Alfredo Martos"}