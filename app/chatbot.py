from openai import OpenAI
import os
from typing import Dict

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_chatbot_response(user_input: str) -> Dict:
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are a helpful car sales assistant. Provide concise, relevant information about vehicles and help customers make informed decisions."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=150
        )
        
        return {
            "response": response.choices[0].message.content,
            "status": "success"
        }
    except Exception as e:
        return {
            "response": str(e),
            "status": "error"
        }