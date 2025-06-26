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

@app.post("/api/passengers", response_model=schemas.Passenger)
def create_passenger(passenger: schemas.PassengerCreate, db: Session = Depends(get_db)):
    return crud.create_passenger(db, passenger)

@app.delete("/api/passengers", response_model=schemas.Message)
def reset_passengers_history(db: Session = Depends(get_db)):
    try:
        deleted = crud.reset_count(db)
        return {"message": f"{deleted} passengers deleted."}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/api/passengers", response_model=list[schemas.Passenger])
def read_all_passengers(db: Session = Depends(get_db)):
    return crud.get_all_passengers(db)

@app.get("/api/passengers/today", response_model=list[schemas.Passenger])
def read_passengers_today(db: Session = Depends(get_db)):
    return crud.get_passengers_today(db)


@app.get("/api/passengers/by_date", response_model=list[schemas.Passenger])
def read_passengers_in_range(
    start_datetime: datetime = Query(..., description="Fecha y hora de inicio (ej: 2025-06-04T08:00:00)"),
    end_datetime: datetime = Query(..., description="Fecha y hora de fin (ej: 2025-06-04T18:00:00)"),
    db: Session = Depends(get_db)
):
    return crud.get_passengers_in_range(db, start_datetime, end_datetime)

@app.websocket("/ws/passenger-count")
async def websocket_passenger_count(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Nueva sesión DB por loop
            db = SessionLocal()
            try:
                count = crud.count_passengers_today(db)
                await websocket.send_json({"count": count})
            finally:
                db.close()

            await asyncio.sleep(2)  # cada 2 segundos (ajustable)
    except WebSocketDisconnect:
        print("Cliente desconectado del stream.")
