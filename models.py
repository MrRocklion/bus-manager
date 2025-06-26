from sqlalchemy import Column, Integer, DateTime, Boolean
from sqlalchemy.sql import func
from database import Base

class Passenger(Base):
    __tablename__ = "passengers"

    id = Column(Integer, primary_key=True, index=True)
    datetime = Column(DateTime, index=True, default=func.now()) 
    special = Column(Boolean, default=False, index=True)
