from groq import Groq
import os
from typing import Dict
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def get_api_key():
    logging.debug("Fetching API key...")
    if os.path.exists('/run/secrets/groq_api_key'):
        with open('/run/secrets/groq_api_key', 'r') as f:
            logging.debug("API key found in secrets.")
            return f.read().strip()
    api_key = os.getenv('GROQ_API_KEY')
    if api_key:
        logging.debug("API key fetched from environment variables.")
    else:
        logging.warning("API key not found.")
    return api_key

def get_inventory() -> str:
    try:
        logging.debug("Fetching inventory from the API...")
        response = requests.get("http://backend:8000/api/vehicles", timeout=10)  # Timeout for API call
        response.raise_for_status()  # Raise an error if the response status is not 200
        inventory = response.json()
        logging.debug(f"Inventory fetched successfully: {len(inventory)} items.")

        # Format inventory into a readable string
        inventory_text = "Current available vehicles:\n"
        for vehicle in inventory:
            inventory_text += f"- {vehicle['año']} {vehicle['marca']} {vehicle['modelo']}: "
            inventory_text += f"${vehicle['precio']:,.2f}, {vehicle['estado']}, {vehicle['disponibilidad']}\n"

        return inventory_text
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching inventory: {e}")
        return "Unable to fetch current inventory. "
    except Exception as e:
        logging.error(f"Unexpected error in get_inventory(): {e}")
        return "An error occurred while fetching inventory."

# Initialize the Groq client
logging.debug("Initializing Groq client...")
client = Groq(api_key=get_api_key())
if client:
    logging.debug("Groq client initialized successfully.")

def get_chatbot_response(user_input: str) -> Dict:
    try:
        logging.debug(f"Received user input: {user_input}")

        # Get current inventory
        inventory = get_inventory()
        logging.debug(f"Formatted inventory:\n{inventory}")

        # Create system prompt with inventory
        system_prompt = f"""You are a helpful car sales assistant. You have access to our current inventory:

{inventory}

Please provide concise, relevant information about vehicles based on our actual inventory. 
When discussing prices or availability, only reference the vehicles we actually have.
If a customer asks about a vehicle we don't have, politely let them know and suggest similar available alternatives from our inventory.
"""

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
