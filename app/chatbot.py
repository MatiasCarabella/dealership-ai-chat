from groq import Groq
import os
from typing import Dict
import logging
from app.database import SessionLocal
from app.models import Vehicle

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Store session-level memory
conversation_memory = {}

def get_api_key():
    logging.debug("Fetching API key...")
    api_key = os.getenv('GROQ_API_KEY')
    if api_key:
        logging.debug("API key fetched from environment variables.")
    else:
        logging.warning("API key not found.")
    return api_key

def get_vehicles() -> str:
    """Fetch vehicles directly from the database."""
    try:
        db = SessionLocal()
        vehicles = db.query(Vehicle).all()  # Query the Vehicle model
        db.close()

        inventory = []
        for vehicle in vehicles:
            inventory.append({
                "year": vehicle.year,  # Updated field names
                "make": vehicle.make,  # Updated field names
                "model": vehicle.model,  # Updated field names
                "price": float(vehicle.price),  # Convert Decimal to float
                "state": vehicle.state.name,  # Convert Enum to string (name)
                "availability": vehicle.availability.name  # Convert Enum to string (name)
            })
        
        inventory_text = "Current available vehicles:\n"
        for vehicle in inventory:
            inventory_text += f"- {vehicle['year']} {vehicle['make']} {vehicle['model']}: "
            inventory_text += f"${vehicle['price']:,.2f}, {vehicle['state']}, {vehicle['availability']}\n"
        
        return inventory_text
    except Exception as e:
        logging.error(f"Error fetching vehicles from database: {str(e)}")
        return "Unable to fetch vehicles."


# Initialize the Groq client
logging.debug("Initializing Groq client...")
client = Groq(api_key=get_api_key())
if client:
    logging.debug("Groq client initialized successfully.")

def get_chatbot_response(user_input: str) -> Dict:
    try:
        # Add user input to memory
        conversation_memory['last_input'] = user_input
        logging.debug(f"Storing user input in memory: {user_input}")

        # Get current inventory
        inventory = get_vehicles()
        
        # Build dynamic system prompt, including user input and memory
        system_prompt = f"""You are a helpful car sales assistant. You have access to our current inventory:

{inventory}

Please provide concise, relevant information about vehicles based on our actual inventory. 
When discussing prices or availability, only reference the vehicles we actually have.
If a customer asks about a vehicle we don't have, politely let them know and suggest similar available alternatives from our inventory.

Previous user query: {conversation_memory.get('last_input', 'No previous query')}

Important: Please avoid using newline characters ('\\n') in your response. Format your response in a single line, with information separated by commas or other appropriate delimiters.
"""
        logging.debug(f"Generated system prompt: {system_prompt}")

        # Sending request to Groq API with system prompt
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
            max_tokens=450,  # To allow for longer responses
            top_p=1,
            stream=False
        )
        logging.debug("Response received from Groq API.")

        # Store response in memory for later use (e.g., referring back to the last response)
        conversation_memory['last_response'] = response.choices[0].message.content

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

