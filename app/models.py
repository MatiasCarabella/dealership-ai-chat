from sqlalchemy import Column, Integer, String, Enum
from app.database import Base

class Vehicle(Base):
    __tablename__ = 'vehicles'

    id = Column(Integer, primary_key=True, index=True)
    marca = Column(String, index=True)
    modelo = Column(String, index=True)
    año = Column(Integer)
    precio = Column(String)
    estado = Column(Enum('nuevo', 'usado'))
    disponibilidad = Column(Enum('disponible', 'no disponible'))
