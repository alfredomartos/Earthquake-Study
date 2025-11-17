This is a backend service that ingests real-time earthquake data from the USGS, stores it in a PostgreSQL database, and exposes it via a containerized RESTful API.

CORE FEATURES

RESTful API: Exposes endpoints to GET all earthquakes or GET one by ID.
Data Ingestion: Automatically fetches and saves new earthquake data from the USGS.
Real-time Simulation: A background task refreshes the data every 10 seconds.
Filtering: The GET /earthquakes endpoint supports filtering by minimum magnitude and start date/time.
Pagination: The GET /earthquakes endpoint is paginated using skip and limit.
Auto-Documentation: Automatic, interactive API documentation is provided by Swagger UI.
Containerized: The entire application (API + Database) is fully containerized with Docker and Docker Compose.

TECH STACK

Backend: Python 3.11, FastAPI, Uvicorn
Database: PostgreSQL 14
ORM: SQLAlchemy
Data Validation: Pydantic
Containerization: Docker & Docker Compose
API Client (Internal): requests

SETUP

PREREQUISITES
Git
Docker Desktop (must be open and running)

1- Clone the Repository
2- Run with Docker Compose
Code: docker-compose up --build
3- http://localhost:8000/docs

ASSUMPTIONS AND LIMITATIONS

Assumptions: I assumed the USGS API is the single source of truth and is generally reliable.
Error Handling: The ingestion task has basic try...except blocks. For a production system, failed ingestion tasks (e.g., if the USGS API is down) should be sent to a retry queue instead of just being logged to the console.
Scalability: The asyncio background task is simple and effective for this scale. For a high-volume system, this task would be moved to a separate, dedicated worker to ensure data ingestion never impacts the API's web traffic performance.
