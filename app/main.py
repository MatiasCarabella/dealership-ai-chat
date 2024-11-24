from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Dict
from pydantic import ValidationError
from fastapi.responses import JSONResponse

from app.database import SessionLocal, engine
from app.models import (
    Vehicle, Base, VehicleCreate, 
    VehicleResponse, ChatInput
)
from app.chatbot import get_chatbot_response

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Dealership AI Chat",
    description="APIs for managing vehicle inventory plus an AI salesman chatbot",
    version="1.0.0"
)

# Configure CORS - Consider restricting origins in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cache the database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Custom exception handler
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()}
    )

@app.get("/api", status_code=status.HTTP_200_OK)
async def root():
    """
    Root endpoint returning API welcome message
    """
    return {
        "message": "Welcome to the Vehicle Dealership API"
    }

@app.get(
    "/api/vehicles", 
    response_model=List[VehicleResponse],
    status_code=status.HTTP_200_OK
)
async def get_vehicles(
    db: Session = Depends(get_db)
):
    """
    Get all vehicles
    """
    vehicles = db.query(Vehicle).all()
    return vehicles

@app.get(
    "/api/vehicles/{vehicle_id}", 
    response_model=VehicleResponse,
    status_code=status.HTTP_200_OK,
    responses={404: {"description": "Vehicle not found"}}
)
async def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    """
    Get a specific vehicle by ID
    """
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if vehicle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Vehicle with ID {vehicle_id} not found"
        )
    return vehicle

@app.post(
    "/api/vehicles", 
    response_model=VehicleResponse,
    status_code=status.HTTP_201_CREATED,
    response_description="Vehicle created successfully"
)
async def create_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db)):
    """
    Create a new vehicle
    """
    try:
        db_vehicle = Vehicle(**vehicle.dict())
        db.add(db_vehicle)
        db.commit()
        db.refresh(db_vehicle)
        return db_vehicle
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create vehicle: {str(e)}"
        )
    
@app.patch(
    "/api/vehicles/{vehicle_id}", 
    response_model=VehicleResponse,
    status_code=status.HTTP_200_OK,
    responses={404: {"description": "Vehicle not found"}}
)
async def partial_update_vehicle(
    vehicle_id: int, 
    updated_fields: dict, 
    db: Session = Depends(get_db)
):
    """
    Update an existing vehicle by ID
    """
    # Fetch the existing vehicle
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if vehicle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle with ID {vehicle_id} not found"
        )

    # Prevent updating the 'id' field
    if "id" in updated_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Updating the 'id' field is not allowed"
        )

    # Validation logic
    valid_states = ["new", "used"]  # Example enum values for 'state'
    valid_availability = ["available", "no available"]  # Example enum values for 'availability'

    try:
        # Apply updates from the request
        for key, value in updated_fields.items():
            if not hasattr(vehicle, key):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Field '{key}' is not a valid attribute of Vehicle"
                )
            
            # Additional field-specific validations
            if key == "state" and value not in valid_states:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid value '{value}' for 'state'. Valid options: {valid_states}"
                )
            if key == "availability" and value not in valid_availability:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid value '{value}' for 'availability'. Valid options: {valid_availability}"
                )
            
            # Apply the update
            setattr(vehicle, key, value)
        
        # Commit changes to the database
        db.commit()
        db.refresh(vehicle)  # Refresh to get updated values
        return vehicle
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update vehicle: {str(e)}"
        )

@app.delete(
    "/api/vehicles/{vehicle_id}", 
    response_model=Dict,
    status_code=status.HTTP_200_OK,
    responses={404: {"description": "Vehicle not found"}}
)
async def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    """
    Delete a vehicle by ID
    """
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    
    if vehicle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Vehicle with ID {vehicle_id} not found"
        )
    
    vehicle_details = {
        "id": vehicle.id,
        "make": vehicle.make,
        "model": vehicle.model,
        "year": vehicle.year,
        "price": float(vehicle.price),
        "state": vehicle.state.name,
        "availability": vehicle.availability.name
    }

    try:
        db.delete(vehicle)
        db.commit()
        return {
            "message": f"Vehicle with ID {vehicle_id} deleted successfully",
            "vehicle_details": vehicle_details
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete vehicle: {str(e)}"
        )

@app.post(
    "/api/chat", 
    response_model=Dict,
    status_code=status.HTTP_200_OK,
    response_description="Chatbot response"
)
async def chat_endpoint(chat_input: ChatInput):
    """
    Interact with the AI-powered chatbot
    """
    try:
        response = get_chatbot_response(chat_input.message)
        if response["status"] == "error":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=response["response"]
            )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat service error: {str(e)}"
        )