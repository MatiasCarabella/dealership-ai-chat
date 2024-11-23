from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Dict

from app.database import SessionLocal, engine
from app.models import (
    Vehicle, Base, VehicleCreate, 
    VehicleResponse, ChatInput
)
from app.chatbot import get_chatbot_response

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api")
async def root():
    return {"message": "Welcome to the Vehicle Sales API"}

@app.get("/api/vehicles", response_model=List[VehicleResponse])
def get_inventory(db: Session = Depends(get_db)):
    vehicles = db.query(Vehicle).all()
    return vehicles

@app.get("/api/vehicles/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle

@app.post("/api/vehicles", response_model=VehicleResponse)
def create_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db)):
    db_vehicle = Vehicle(**vehicle.dict())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

@app.delete("/api/vehicles/{vehicle_id}", response_model=Dict)
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    # Store vehicle details before deletion
    vehicle_details = {
        "id": vehicle.id,
        "make": vehicle.make,
        "model": vehicle.model,
        "year": vehicle.year,
        "price": float(vehicle.price),  # Convert Decimal to float
        "state": vehicle.state.name,  # Convert Enum to string
        "availability": vehicle.availability.name  # Convert Enum to string
    }

    db.delete(vehicle)
    db.commit()
    
    # Include the deleted vehicle's details in the response
    return {
        "message": f"Vehicle with id {vehicle_id} deleted successfully.",
        "vehicle_details": vehicle_details
    }


@app.post("/api/chat", response_model=Dict)
async def chat_endpoint(chat_input: ChatInput):
    response = get_chatbot_response(chat_input.message)
    if response["status"] == "error":
        raise HTTPException(status_code=500, detail=response["response"])
    return response
