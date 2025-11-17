# app/api/endpoints.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .. import crud, schemas
from datetime import datetime

from .. import crud
from ..database import get_db

router = APIRouter()

@router.get("/earthquakes", response_model=List[schemas.Earthquake])
def read_earthquakes(
    skip: int = Query(default=0, description="Number of records to skip for pagination"),
    limit: int = Query(default=100, description="Maximum number of records to return"),
    min_magnitude: float | None = Query(
        default=None, 
        description="Filter for magnitudes greater than or equal to this value",
    ),
    start_date: datetime | None = Query(
        default=None, 
        description="Filter by start date. Format (2025-11-13T00:00:00)"
    ),
    end_date: datetime | None = Query(
        default=None,
        description="Filter by end date. Format (2025-11-18T00:00:00)"
    ),
    db: Session = Depends(get_db),
):
    earthquakes = crud.get_earthquakes(
        db,
        skip=skip,
        limit=limit,
        min_magnitude=min_magnitude,
        start_date=start_date,
        end_date=end_date,
    )
    return earthquakes

@router.get("/earthquakes/{id}")
def read_earthquake_detail(id: str, db: Session = Depends(get_db)):
    db_earthquake = crud.get_earthquake(db, earthquake_id=id)
    if db_earthquake is None:
        raise HTTPException(status_code=404, detail="Earthquake not found")
    return db_earthquake

@router.post("/ingest", status_code=201)
def trigger_ingestion(db: Session = Depends(get_db)):
    result = crud.ingest_earthquake_data(db)
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result