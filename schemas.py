from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

class PassengerBase(BaseModel):
    datetime: datetime
    special: bool

class PassengerCreate(BaseModel):
    special: bool 

class Passenger(PassengerBase):
    id: int
    datetime: datetime
    special: bool
    model_config = {
        "from_attributes": True
    }
class Message(BaseModel):
    message: str

class TransactionBase(BaseModel):
    card_code: str
    card_type: int
    date: str
    time: str
    amount: Decimal
    balance: Decimal
    last_balance: Decimal
    uploaded: bool = False

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    timestamp: datetime

    model_config = {
        "from_attributes": True
    }

class MessageResponseTransaction(BaseModel):
    message: str
    status: int
    result: Transaction