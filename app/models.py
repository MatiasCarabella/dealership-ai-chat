from sqlalchemy import Column, Integer, String, Enum, Numeric
from app.database import Base
from pydantic import BaseModel
import enum

# SQLAlchemy Enums
class StateEnum(enum.Enum):
    new = 'new'
    used = 'used'

class AvailabilityEnum(enum.Enum):
    available = 'available'
    not_available = 'not available'

# SQLAlchemy Model
class Vehicle(Base):
    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True, index=True)
    make = Column(String(50), index=True)
    model = Column(String(50), index=True)
    year = Column(Integer)
    price = Column(Numeric(10, 2))
    state = Column(Enum(StateEnum, name='state_enum'))
    availability = Column(Enum(AvailabilityEnum, name='availability_enum'))

# Pydantic Models
class VehicleBase(BaseModel):
    make: str
    model: str
    year: int
    price: float
    state: str  # Will validate against StateEnum values
    availability: str  # Will validate against AvailabilityEnum values

class VehicleCreate(VehicleBase):
    pass

class VehicleResponse(VehicleBase):
    id: int

    class Config:
        from_attributes = True

class ChatInput(BaseModel):
    message: str
