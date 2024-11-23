import openai

openai.api_key = "your-openai-api-key-here"

def get_chatbot_response(user_input: str):
    response = openai.Completion.create(
        engine="text-davinci-003",  
        prompt=user_input,  
        max_tokens=150,  
        temperature=0.7  
    )
    return response.choices[0].text.strip()
