# app/app/schemas.py
from pydantic import BaseModel, field_serializer
from datetime import datetime

class EarthquakeBase(BaseModel):
    id: str
    location: str
    magnitude: float
    depth: float
    date: datetime

class EarthquakeCreate(EarthquakeBase):
    pass

class Earthquake(EarthquakeBase):
    @field_serializer('date')
    def serialize_date(self, date_obj: datetime, _info):
        return date_obj.strftime("%d-%m-%Y %H:%M:%S")
    
    class Config:
        from_attributes = True