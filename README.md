<div id="user-content-toc">
  <ul align="center" style="list-style: none;">
    <summary>
      <h1 align="center"> Dealership AI ֎</h1>
    </summary>
  </ul>
</div>
<div align="center">
   <a href="https://www.python.org/" target="_blank"><img src="https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=fff" alt="Python" /></a>
    <a href="https://fastapi.tiangolo.com/" target="_blank"><img src="https://img.shields.io/badge/FastAPI-009485.svg?logo=fastapi&logoColor=white" alt="FastAPI" /></a>
   <a href="https://www.postgresql.org/" target="_blank"><img src="https://img.shields.io/badge/Postgres-17-blue?logo=postgresql&logoColor=white" alt="Postgres" /></a>
   <a href="https://www.docker.com/" target="_blank"><img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=fff" alt="Docker" /></a>
</div>
<h1></h1>

API-driven application featuring an AI-powered chatbot designed to assist or replace sales representatives at car dealerships. It uses AI to provide customers with detailed information about available vehicles, answer their queries, and offer tailored suggestions based on the dealership's inventory.

## Features

- **AI-Powered Chatbot**: Provides intelligent, context-aware responses.
- **Real-Time Inventory Integration**: Fetches vehicle details directly from the database.
- **Dockerized Deployment**: Easy-to-deploy solution requiring minimal setup.

## Setup Instructions

### Prerequisites
- [Docker](https://docs.docker.com/get-started/get-docker/) and [Docker Compose](https://docs.docker.com/compose/)
- API key for [**Groq**](https://console.groq.com/docs/overview) (AI provider)

### Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/dealership-ai-chat.git
cd dealership-ai-chat
```

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

4. Access the application on http://localhost:8000/api.

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

Endpoint | Method | Description
--- | --- | ---
`/api` | **GET** | 	Welcome message
`/api/vehicles` | **GET** | 	Get all vehicles
`/api/vehicles/{id}` | **GET** | 	Get a vehicle by ID
`/api/vehicles` | **POST** | 	Create a vehicle
`/api/vehicles/{id}` | **PATCH** | 	Update a vehicle by ID
`/api/vehicles/{id}` | **DELETE** | 	Delete a vehicle by ID
`/api/chat` | **POST** | 	Interact with the AI-powered chatbot

[API Documentation (Postman)](https://documenter.getpostman.com/view/10146128/2sAYBUDCCW)

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
Follow-up Request:
```json
{
    "message": "Yes please! Tell me about the Corolla"
}
```
Response:
```json
{
    "status": "success",
    "response": "The 2021 Toyota Corolla is a new vehicle in our inventory, and it's priced at $20,000. This compact sedan is known for its reliability, fuel efficiency, and comfortable ride. It comes with a variety of standard features, including a 7-inch touchscreen infotainment system, Android Auto and Apple CarPlay compatibility, and automatic climate control. The Corolla also offers a hybrid version if you're interested in increased fuel efficiency. Overall, the Toyota Corolla is a great option for those looking for a dependable and well-equipped sedan. Let me know if you'd like to schedule a test drive or if you have any questions about financing options."
}
```

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- [**FastAPI**](https://fastapi.tiangolo.com/) ⚡ for the backend framework.
- [**Docker**](https://www.docker.com/) 🐳 for containerized deployment.
- [**Groq**](https://groq.com/) 🧠 for the AI services.
