import requests
from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

def get_earthquake(db: Session, earthquake_id: str):
    return db.query(models.Earthquake).filter(models.Earthquake.id == earthquake_id).first()

def get_earthquakes(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    min_magnitude: float | None = None,
    start_date: datetime | None = None,
    end_date: datetime | None = None
):
    query = db.query(models.Earthquake)

    if min_magnitude is not None:
        query = query.filter(models.Earthquake.magnitude >= min_magnitude)

    if start_date is not None:
        query = query.filter(models.Earthquake.date >= start_date)

    if end_date is not None:
        query = query.filter(models.Earthquake.date <= end_date)

    query = query.order_by(models.Earthquake.date.desc()) \
                 .offset(skip) \
                 .limit(limit)

    return query.all()

USGS_API_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"

def ingest_earthquake_data(db: Session):
    try:
        response = requests.get(USGS_API_URL)
        response.raise_for_status()
        data = response.json()

        earthquakes_to_add = []

        for item in data.get("features", []):
            try:
                props = item.get("properties", {})
                coords = item.get("geometry", {}).get("coordinates", [])

                mag = props.get("mag")
                time_ms = props.get("time")
                place = props.get("place")

                if (mag is None) or (time_ms is None) or (place is None) or (len(coords) != 3):
                    print(f"Skipping item {item.get('id')} due to incomplete data.")
                    continue
                time_datetime = datetime.utcfromtimestamp(time_ms / 1000.0)

                earthquake_data = schemas.EarthquakeCreate(
                    id=item.get("id"),
                    location=place,
                    magnitude=mag,
                    depth=coords[2],
                    date=time_datetime
                )

                existing = get_earthquake(db, earthquake_id=earthquake_data.id)
                if not existing:
                    earthquakes_to_add.append(earthquake_data)

            except Exception as e:
                print(f"Error processing item {item.get('id')}: {e}")

        for eq_data in earthquakes_to_add:
            db_earthquake = models.Earthquake(**eq_data.dict())
            db.add(db_earthquake)

        if earthquakes_to_add:
            db.commit()
            print(f"Successfully ingested {len(earthquakes_to_add)} earthquakes.")
            return {"status": "success", "ingested": len(earthquakes_to_add)}
        else:
            print("No new earthquakes to ingest.")
            return {"status": "success", "ingested": 0, "message": "No new earthquakes"}

    except requests.RequestException as e:
        print(f"Error fetching from USGS: {e}")
        return {"status": "error", "message": str(e)}