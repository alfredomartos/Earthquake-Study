from sqlalchemy import Column, String, Float, DateTime 
from .database import Base

class Earthquake(Base):
    __tablename__ = "earthquakes"

    id = Column(String, primary_key=True, index=True)
    location = Column(String)
    magnitude = Column(Float, index=True)
    depth = Column(Float)
    date = Column(DateTime, index=True)