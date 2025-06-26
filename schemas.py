from pydantic import BaseModel
from datetime import datetime

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
