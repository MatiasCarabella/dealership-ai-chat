from sqlalchemy import Column, Integer, String, Enum, Numeric
from app.database import Base
from pydantic import BaseModel
import enum

# SQLAlchemy Enums
class EstadoEnum(enum.Enum):
    nuevo = 'nuevo'
    usado = 'usado'

class DisponibilidadEnum(enum.Enum):
    disponible = 'disponible'
    no_disponible = 'no disponible'

# SQLAlchemy Model
class Vehicle(Base):
    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True, index=True)
    marca = Column(String(50), index=True)
    modelo = Column(String(50), index=True)
    año = Column(Integer)
    precio = Column(Numeric(10, 2))
    estado = Column(Enum(EstadoEnum, name='estado_enum'))
    disponibilidad = Column(Enum(DisponibilidadEnum, name='disponibilidad_enum'))

# Pydantic Models
class VehicleBase(BaseModel):
    marca: str
    modelo: str
    año: int
    precio: float
    estado: str  # Will validate against EstadoEnum values
    disponibilidad: str  # Will validate against DisponibilidadEnum values

class VehicleCreate(VehicleBase):
    pass

class VehicleResponse(VehicleBase):
    id: int

    class Config:
        from_attributes = True

class ChatInput(BaseModel):
    message: str