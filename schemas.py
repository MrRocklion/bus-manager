from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import List, Any,Optional

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


class MessageResponsePassenger(BaseModel):
    message: str
    status: int
    result: Passenger

    model_config = {
        "from_attributes": True
    }


class MessageResponseListPassenger(BaseModel):
    message: str
    status: int
    result: List[Passenger]
    
    model_config = {
        "from_attributes": True
    }



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
    
    model_config = {
        "from_attributes": True
    }


class MessageResponseListTransaction(BaseModel):
    message: str
    status: int
    result: List[Transaction]

    model_config = {
        "from_attributes": True
    }


class TransactionFormatted(BaseModel):
    id: int
    card_code: str
    card_type: int
    date: str
    time: str
    amount: float
    balance: float
    last_balance: float
    timestamp: str

class TransactionListResponse(BaseModel):
    message: str
    status: int
    result: List[TransactionFormatted]

    model_config = {
        "from_attributes": True
    }

class MessageResponseDict(BaseModel):
    message: str
    status: int
    result: Any



class Point(BaseModel):
    x: int
    y: int

class CounterConfigBase(BaseModel):
    cross_line_y: int
    excluded_areas: Optional[List[List[Point]]] = None
    track_threshold: float = 0.40
    track_buffer: int = 70
    ip_counter_camera: str
    ip_back_camera: str
    ip_front_camera: str
    user_camera: str
    password_camera: str

class CounterConfigCreate(CounterConfigBase):
    pass

class CounterConfig(CounterConfigBase):
    id: int

    model_config = {
        "from_attributes": True
    }

class MessageResponseCounterConfig(BaseModel):
    message: str
    status: int
    result: CounterConfig

    model_config = {
        "from_attributes": True
    }

class MessageResponseListCounterConfig(BaseModel):
    message: str
    status: int
    result: List[CounterConfig]
    model_config = {
        "from_attributes": True
    }