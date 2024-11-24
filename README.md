# Dealership AI

API-driven application featuring an AI-powered chatbot designed to assist or replace sales representatives at car dealerships. It uses AI to provide customers with detailed information about available vehicles, answer their queries, and offer tailored suggestions based on the dealership's inventory.

## Features

- **AI-Powered Chatbot**: Provides intelligent, context-aware responses.
- **Real-Time Inventory Integration**: Fetches vehicle details directly from the database.
- **Dockerized Deployment**: Easy-to-deploy solution requiring minimal setup.

## Getting Started

### Prerequisites
- [Docker](https://docs.docker.com/get-started/get-docker/) and [Docker Compose](https://docs.docker.com/compose/)
- API key for [**Groq**](https://console.groq.com/docs/overview) (AI provider)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/dealership-ai-chat.git
   cd dealership-ai-chat

2. Set up the environment variables:
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file file to set your [Groq API key](https://console.groq.com/docs/overview):
   ```
   GROQ_API_KEY=YOUR_API_KEY_HERE
   ```
3. Build and start the application using Docker Compose:
   ```bash
   docker-compose up --build 
   ```
   _The `init.sql` script automatically sets up the database schema along with sample data during the Docker container build process, so no manual setup is required!_

4. Access the application on [http://localhost:8000/api](http://localhost:8000/api).

## Project Structure
```
dealership-ai-chat/
└── app/
|   ├── __init__.py      # Package initialization
|   ├── main.py          # FastAPI application
|   ├── chatbot.py       # Chatbot implementation
|   ├── database.py      # Database connection and setup
|   └── models.py        # Database models and schemas
├── Dockerfile           # Dockerfile for the app
├── docker-compose.yml   # Docker Compose configuration
├── requirements.txt     # Python dependencies
├── init.sql             # Database initialization script
├── .env.example         # Environment variables
├── .gitignore           # Files to ignore in Git
├── LICENSE              # MIT license
└── README.md            # You're reading it now
```

## Usage
### API Endpoints

[Documentation (Postman)](https://documenter.getpostman.com/view/10146128/2sAYBUDCCW#b3822fed-90b9-45a4-b16d-ddb57b6a1ba8)

Endpoint | Method | Description
--- | --- | ---
`/api` | **GET** | 	Welcome message
`/api/vehicles` | **GET** | 	Get all vehicles
`/api/vehicles/{id}` | **GET** | 	Get a vehicle by ID
`/api/vehicles` | **POST** | 	Add a new vehicle to inventory
`/api/vehicles/{id}` | **DELETE** | 	Delete a vehicle by ID
`/api/chat` | **GET** | 	Interact with the AI-powered chatbot

### Example Chat Interaction
Send a **POST** request to `/api/chat` with the following payload:
```json
{
    "message": "Do you have any Toyotas?"
}
```
Response:
```json
{
    "status": "success",
    "response": "Yes, we do have Toyotas in our current inventory. We have a new 2021 Toyota Corolla available at a price of $20,000.0. Would you like more information on this vehicle or would you like to explore other options as well?"
}
```

## Acknowledgements

- [**FastAPI**](https://fastapi.tiangolo.com/) ⚡ for the backend framework.
- [**Docker**](https://www.docker.com/) 🐳 for containerized deployment.
- [**Groq**](https://groq.com/) 🧠 for the AI services.


## License

This project is licensed under the [MIT License](https://github.com/MatiasCarabella/dealership-ai-chat/blob/main/LICENSE).
