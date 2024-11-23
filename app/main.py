from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models import Vehicle
from app.chatbot import get_chatbot_response

# Initialize database
Vehicle.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/inventory")
def get_inventory(db: Session = Depends(get_db)):
    vehicles = db.query(Vehicle).all()
    return vehicles

@app.post("/chat")
def chat(user_input: str):
    response = get_chatbot_response(user_input)
    return {"response": response}
