from groq import Groq
import os
from typing import Dict, List, Optional
from datetime import datetime
import logging
import json
from pydantic import BaseModel, Field
from app.database import SessionLocal
from app.models import Vehicle

# Configure logging only for our chatbot
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Changed from DEBUG to INFO
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Add handlers with our specific formatting
file_handler = logging.FileHandler('chatbot.log')
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# Prevent logs from propagating to the root logger
logger.propagate = False

class Conversation(BaseModel):
    """Model to track conversation history and context"""
    messages: List[Dict[str, str]] = Field(default_factory=list)
    last_interaction: datetime = Field(default_factory=datetime.now)
    context: Dict = Field(default_factory=dict)

class VehicleQuery(BaseModel):
    """Model to structure vehicle search parameters"""
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    max_price: Optional[float] = None
    state: Optional[str] = None

class Chatbot:
    def __init__(self):
        logger.info("Initializing chatbot...")
        self.client = self._initialize_groq_client()
        self.conversations: Dict[str, Conversation] = {}
        self.model = "mixtral-8x7b-32768"
        
    @staticmethod
    def _get_api_key() -> str:
        """Get API key from environment variables"""
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            logger.error("GROQ_API_KEY not found in environment variables")
            raise ValueError("GROQ_API_KEY not found")
        return api_key

    def _initialize_groq_client(self) -> Groq:
        """Initialize Groq client with error handling"""
        try:
            client = Groq(api_key=self._get_api_key())
            logger.info("Groq client initialized successfully")
            return client
        except Exception as e:
            logger.error(f"Failed to initialize Groq client: {e}")
            raise

    def _get_vehicles(self) -> str:
        """
        Fetch all available vehicles and format them as JSON for AI consumption.
        """
        db = SessionLocal()
        try:
            vehicles = db.query(Vehicle).all()  # Fetch all vehicles from the database
            logger.info(f"Retrieved {len(vehicles)} vehicles from database")
            
            # Create a list of dictionaries for each vehicle
            vehicle_details = [
                {
                    "make": v.make,
                    "model": v.model,
                    "year": v.year,
                    "price": float(v.price),
                    "state": v.state.name,
                    "availability": v.availability.name
                }
                for v in vehicles
            ]
            
            # Convert to JSON string
            inventory_json = json.dumps({
                "vehicles": vehicle_details,
                "total_vehicles": len(vehicle_details)
            }, indent=2)  # Pretty-print JSON for readability
            
            logger.debug(f"Vehicle inventory in JSON format: {inventory_json}")
            return inventory_json
        except Exception as e:
            logger.error(f"Database error: {e}")
            raise
        finally:
            db.close()




    def _build_system_prompt(self, conversation: Conversation, inventory_json: str) -> str:
        """
        Build a dynamic system prompt with JSON-formatted inventory data.
        """
        return f"""You are an experienced car sales assistant at our dealership. Your goal is to help customers find their ideal vehicle while providing accurate information based solely on our current inventory.

Guidelines:
- Use the provided JSON inventory data as your single source of truth
- Match customer requirements to available vehicles
- When exact matches aren't available, recommend similar vehicles from inventory, explaining your reasoning
- Maintain a professional yet friendly tone
- Format responses as continuous text without line breaks

Input Data:
Inventory: {inventory_json}
Conversation History: {conversation.context}"""

    def get_response(self, user_input: str, session_id: str = "default") -> Dict:
        """
        Generate chatbot response with conversation management
        """
        try:
            # Initialize or get existing conversation
            if session_id not in self.conversations:
                logger.info(f"Creating new conversation session: {session_id}")
                self.conversations[session_id] = Conversation()
            
            conversation = self.conversations[session_id]
            conversation.last_interaction = datetime.now()
            
            # Get filtered inventory (now we don't parse the user input)
            inventory = self._get_vehicles()

            # Build prompt and get response
            system_prompt = self._build_system_prompt(conversation, inventory)
            logger.info(f"System prompt: {system_prompt}")
            conversation.messages.append({"role": "user", "content": user_input})
            
            logger.info("Sending request to Groq API")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    *conversation.messages[-5:]
                ],
                temperature=0.7,
                max_tokens=450,
                top_p=1,
                stream=False
            )
            
            response_content = response.choices[0].message.content
            conversation.messages.append({"role": "assistant", "content": response_content})
            logger.info("Successfully generated response from Groq API")
            
            return {"status": "success", "response": response_content}
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {"status": "error", "response": str(e)}

# Initialize singleton instance
chatbot = Chatbot()

def get_chatbot_response(user_input: str) -> Dict:
    """
    Public interface for chatbot functionality
    """
    return chatbot.get_response(user_input)