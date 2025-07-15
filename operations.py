import models, schemas
import pytz
from typing import List
from models import Passenger
from sqlalchemy.orm import Session
from datetime import datetime, date
def create_passenger(db: Session, passenger: schemas.PassengerCreate):
    ecu_time = datetime.now(pytz.timezone("America/Guayaquil")).replace(microsecond=0)

    db_passenger = models.Passenger(
        datetime=ecu_time,
        special=passenger.special
    )
    db.add(db_passenger)
    db.commit()
    db.refresh(db_passenger)
    return db_passenger

def create_transaction(db: Session, tx_data: schemas.TransactionCreate):
    ecu_time = datetime.now(pytz.timezone("America/Guayaquil")).replace(microsecond=0)

    tx = models.Transaction(
        card_code=tx_data.card_code,
        card_type=tx_data.card_type,
        date=tx_data.date,
        time=tx_data.time,
        amount=tx_data.amount,
        balance=tx_data.balance,
        last_balance=tx_data.last_balance,
        timestamp=ecu_time,
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx

def get_all_passengers(db: Session):
    return db.query(models.Passenger).all()

def reset_count(db: Session):
    deleted = db.query(models.Passenger).delete()
    db.commit()
    return deleted


def get_passengers_today(db: Session) -> List[Passenger]:
    today = date.today()
    return db.query(Passenger).filter(
        Passenger.datetime >= datetime.combine(today, datetime.min.time()),
        Passenger.datetime <= datetime.combine(today, datetime.max.time())
    ).all()

def count_passengers_today(db: Session) -> int:
    today = date.today()
    return db.query(Passenger).filter(
        Passenger.datetime >= datetime.combine(today, datetime.min.time()),
        Passenger.datetime <= datetime.combine(today, datetime.max.time())
    ).count()

def get_passengers_in_range(db: Session, start_datetime: datetime, end_datetime: datetime) -> List[Passenger]:
    return db.query(Passenger).filter(
        Passenger.datetime >= start_datetime,
        Passenger.datetime <= end_datetime
    ).all()

def get_transactions_in_range(db: Session, start_datetime: datetime, end_datetime: datetime) -> List[models.Transaction]:
    return db.query(models.Transaction).filter(
        models.Transaction.timestamp >= start_datetime,
        models.Transaction.timestamp <= end_datetime
    ).all()