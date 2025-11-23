from pydantic import BaseModel
from database import Base 
from sqlalchemy import Column, Integer, String, Float

class OfferDB(Base):
    __tablename__ = "offers"
    id = Column(Integer, primary_key=True)
    area_m2 = Column(Float)
    rooms = Column(Integer)
    photos = Column(Integer)
    locality = Column(String)
    street = Column(String)
    property_type = Column(String)
    city = Column(String)
    price = Column(Float)

# Pydantic model
class Offer(BaseModel):
    area_m2: float
    rooms: int
    photos: int
    locality: str
    street: str
    property_type: str
    city: str
    price: float

    class Config:
        orm_mode = True

class OfferCreate(BaseModel):
    area_m2: float
    rooms: int
    photos: int
    locality: str
    street: str
    property_type: str
    city: str
    price: float

class PricePrediction(BaseModel):
    area_m2: float
    rooms: int
    photos: int
    locality: str
    street: str
    property_type: str
    city: str
    price: float