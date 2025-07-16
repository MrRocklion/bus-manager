import models, schemas, operations as crud
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends,Query,HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from datetime import datetime

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/api/passengers", response_model=schemas.MessageResponsePassenger)
def create_passenger(passenger: schemas.PassengerCreate, db: Session = Depends(get_db)):
    result = crud.create_passenger(db, passenger)
    return {
        "message": "Passenger created successfully",
        "status": 201,
        "result": result
    }




@app.post("/api/transactions", response_model=schemas.MessageResponseTransaction)
def create_transaction(tx_data: schemas.TransactionCreate, db: Session = Depends(get_db)):
    result = crud.create_transaction(db, tx_data)
    return {
        "message": "Transaction created successfully",
        "status": 201,
        "result": result
    }


@app.post("/api/counter_configs", response_model=schemas.MessageResponseCounterConfig)
def create_counter_config_route(
    config_data: schemas.CounterConfigCreate,
    db: Session = Depends(get_db)
):
    cfg = crud.create_counter_config(db, config_data)
    return {
        "message": "Counter configuration created successfully",
        "status": 201,
        "result": cfg
    }



@app.delete("/api/passengers", response_model=schemas.MessageResponseDict)
def reset_passengers_history(db: Session = Depends(get_db)):
    try:
        deleted = crud.reset_count(db)
        result = {"message": f"{deleted} passengers deleted."}
        return {
            "message": "Passengers history reset successfully",
            "status": 200,
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@app.delete("/api/transactions", response_model=schemas.MessageResponseDict)
def reset_transactions_history(db: Session = Depends(get_db)):
    try:
        deleted = crud.reset_transactions(db)
        result = {"message": f"{deleted} transactions deleted."}
        return {
            "message": "Transactions history reset successfully",
            "status": 200,
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/api/passengers", response_model=schemas.MessageResponseListPassenger)
def read_all_passengers(db: Session = Depends(get_db)):
    result = crud.get_all_passengers(db)
    return {
        "message": "All Passengers retrieved successfully",
        "status": 200,
        "result": result
    }

@app.get("/api/passengers/today", response_model=schemas.MessageResponseListPassenger)
def read_passengers_today(db: Session = Depends(get_db)):
    result = crud.get_passengers_today(db)
    return {
        "message": "Passengers for today retrieved successfully",
        "status": 200,
        "result": result
    }


@app.get("/api/passengers/by_date", response_model=schemas.MessageResponseListPassenger)
def read_passengers_in_range(
    start_datetime: datetime = Query(..., description="Fecha y hora de inicio"),
    end_datetime: datetime = Query(..., description="Fecha y hora de fin"),
    db: Session = Depends(get_db)
):
    result = crud.get_passengers_in_range(db, start_datetime, end_datetime)
    return {
        "message": "Passengers in range retrieved successfully",
        "status": 200,
        "result": result
    }



@app.get("/api/transactions/by_date", response_model=schemas.MessageResponseListTransaction)
def get_transactions_by_dates(
        start_datetime: datetime = Query(..., description="Fecha y hora de inicio"),
        end_datetime: datetime = Query(..., description="Fecha y hora de fin"),
        db: Session = Depends(get_db)
    ):
    result = crud.get_transactions_in_range(db, start_datetime, end_datetime)
    if not result:
        raise HTTPException(status_code=404, detail="No transactions found in the specified range.")
    return {
        "message": "Transactions retrieved successfully",
        "status": 200,
        "result": result
    }



@app.get("/api/transactions/today", response_model=schemas.MessageResponseListTransaction)
def get_transactions_today(db: Session = Depends(get_db)):
    result = crud.get_transactions_today(db)
    return {
        "message": "Transactions for today retrieved successfully",
        "status": 200,
        "result": result
    }

@app.get("/api/counter_configs", response_model=schemas.MessageResponseListCounterConfig)
def get_all_counter_configs(db: Session = Depends(get_db)):
    result = crud.get_all_counter_configs(db)
    return {
        "message": "All counter configurations retrieved successfully",
        "status": 200,
        "result": result
    }



@app.get("/api/counter_configs/last", response_model=schemas.MessageResponseCounterConfig)
def get_last_counter_config(db: Session = Depends(get_db)):
    result = crud.get_last_counter_config(db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró ninguna configuración de contador"
        )
    return {
        "message": "Last counter configuration retrieved successfully",
        "status": 200,
        "result": result
    }



@app.websocket("/ws/passenger-count")
async def websocket_passenger_count(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            db = SessionLocal()
            try:
                count = crud.count_passengers_today(db)
                await websocket.send_json({"count": count})
            finally:
                db.close()

            await asyncio.sleep(0.5)  # cada 2 segundos (ajustable)
    except WebSocketDisconnect:
        print("Cliente desconectado del stream.")