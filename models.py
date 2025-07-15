from sqlalchemy import Column, Integer, DateTime, Boolean,String,Numeric
from sqlalchemy.sql import func
from database import Base

class Passenger(Base):
    __tablename__ = "passengers"

    id = Column(Integer, primary_key=True, index=True)
    datetime = Column(DateTime, index=True, default=func.now()) 
    special = Column(Boolean, default=False, index=True)

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
    