from sqlalchemy import Column, Integer, DateTime, Boolean,String,Numeric,Float,JSON
from sqlalchemy.sql import func
from database import Base

class Passenger(Base):
    __tablename__ = "passengers"

    id = Column(Integer, primary_key=True, index=True)
    datetime = Column(DateTime, index=True, default=func.now()) 
    special = Column(Boolean, default=False, index=True)
    uploaded = Column(Boolean, default=False, index=True)

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer,primary_key = True,index=True)
    card_code = Column(String,index=True,nullable=False)
    card_type = Column(String,index=True,nullable=False)
    date =Column(String,index=True,nullable=False)
    time = Column(String,index=True,nullable=False)
    amount = Column(Numeric,index=True,nullable=False)
    balance = Column(Numeric,index=True,nullable=False)
    last_balance = Column(Numeric,index=True,nullable=False)
    timestamp = Column(DateTime, index=True)
    uploaded = Column(Boolean, default=False, index=True)

class CounterConfig(Base):
    __tablename__ = "counter_config"
    id = Column(Integer, primary_key=True, index=True)
    cross_line_y = Column(Integer, nullable=False)
    excluded_areas = Column(JSON, nullable=True)
    track_threshold = Column(Float, nullable=False, default=0.40)
    track_buffer = Column(Integer, nullable=False, default=70)
    timestamp = Column(DateTime, index=True, default=func.now())
    ip_counter_camera = Column(String, nullable=False)
    ip_back_camera = Column(String, nullable=False)
    ip_front_camera = Column(String, nullable=False)
    user_camera = Column(String, nullable=False)
    password_camera = Column(String, nullable=False)
