from groq import Groq
import os
from typing import Dict
import logging
from app.database import SessionLocal
from app.models import Vehicle

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def get_api_key():
    logging.debug("Fetching API key...")
    api_key = os.getenv('GROQ_API_KEY')
    if api_key:
        logging.debug("API key fetched from environment variables.")
    else:
        logging.warning("API key not found.")
    return api_key

def get_inventory() -> str:
    """Fetch inventory directly from the database."""
    try:
        db = SessionLocal()
        vehicles = db.query(Vehicle).all()  # Query the Vehicle model
        db.close()

        inventory = []
        for vehicle in vehicles:
            inventory.append({
                "year": vehicle.año,
                "make": vehicle.marca,
                "model": vehicle.modelo,
                "price": float(vehicle.precio),  # Convert Decimal to float
                "state": vehicle.estado.name,  # Convert Enum to string (name)
                "availability": vehicle.disponibilidad.name  # Convert Enum to string (name)
            })
        
        inventory_text = "Current available vehicles:\n"
        for vehicle in inventory:
            inventory_text += f"- {vehicle['year']} {vehicle['make']} {vehicle['model']}: "
            inventory_text += f"${vehicle['price']:,.2f}, {vehicle['state']}, {vehicle['availability']}\n"
        
        return inventory_text
    except Exception as e:
        logging.error(f"Error fetching inventory from database: {str(e)}")
        return "Unable to fetch inventory."

# Initialize the Groq client
logging.debug("Initializing Groq client...")
client = Groq(api_key=get_api_key())
if client:
    logging.debug("Groq client initialized successfully.")

def get_chatbot_response(user_input: str) -> Dict:
    try:
        # Get current inventory
        inventory = get_inventory()
        
        # Log the system prompt for debugging (optional)
        system_prompt = f"""You are a helpful car sales assistant. You have access to our current inventory:

{inventory}

Please provide concise, relevant information about vehicles based on our actual inventory. 
When discussing prices or availability, only reference the vehicles we actually have.
If a customer asks about a vehicle we don't have, politely let them know and suggest similar available alternatives from our inventory.
"""
        logging.debug(f"Generated system prompt: {system_prompt}")

        logging.debug("Sending request to Groq API...")
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {
                    "role": "system", 
                    "content": system_prompt
                },
                {
                    "role": "user", 
                    "content": user_input
                }
            ],
            temperature=0.7,
            max_tokens=300,  # Increased to allow for longer responses
            top_p=1,
            stream=False
        )
        logging.debug("Response received from Groq API.")

        return {
            "response": response.choices[0].message.content,
            "status": "success"
        }
    except Exception as e:
        logging.error(f"Error in get_chatbot_response(): {e}")
        return {
            "response": str(e),
            "status": "error"
        }
