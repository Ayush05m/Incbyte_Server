# FastAPI Shop Backend

This project is a backend for a shop built with FastAPI, PostgreSQL, and other modern technologies. It includes features like JWT authentication, password hashing, and asynchronous endpoints. The project is fully containerized with Docker for easy setup and deployment.

## Features
- FastAPI framework
- PostgreSQL with SQLAlchemy
- Alembic for migrations
- JWT authentication
- Bcrypt password hashing
- Async endpoints
- Full TDD coverage (pytest, httpx)
- Containerized with Docker
- AI co-authorship (Claude, ChatGPT, Copilot, Dyad, Gemini, Grok)

## Prerequisites

Before you begin, ensure you have [Docker](https://www.docker.com/get-started) installed on your system.

## Getting Started with Docker (Recommended)

This is the recommended way to run the application for both development and production.

### 1. Environment Variables

Create a `.env` file in the root of the project and add the following environment variables. Replace the values with your actual database credentials and a strong secret key.

```
DATABASE_URL=postgresql+asyncpg://user:password@host/dbname
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
RAZORPAY_KEY_ID=your-key-id
RAZORPAY_KEY_SECRET=your-key-secret
```

### 2. Running the Application

With Docker and Docker Compose installed, you can start the application with a single command:

```bash
docker-compose up -d
```

This will build the Docker image and start the application container in detached mode. The application will be available at `http://localhost:8000`.

### 3. Stopping the Application

To stop the application, run:

```bash
docker-compose down
```

### 4. Viewing Logs

To view the application logs, run:

```bash
docker-compose logs
```

## Manual Setup (for development)

If you prefer to run the application without Docker, you can follow these steps.

### 1. Installation

1.  Clone the repository.
2.  Create and activate a Python virtual environment.
3.  Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### 2. Running the Server

```bash
uvicorn app.main:app --reload
```

### 3. Alembic Migrations

-   Initialize Alembic: `alembic init alembic`
-   Edit `alembic.ini` and `env.py` for your PostgreSQL connection.
-   Create a migration: `alembic revision --autogenerate -m "Initial migration"`
-   Apply the migration: `alembic upgrade head`

### 4. Running Tests

```bash
$env:PYTHONPATH="<your_project_file_location>"; pytest app/tests/api/routes/
```

## Deployment to GCP

This containerized application can be deployed to Google Cloud Platform (GCP) using several services:

-   **Google Cloud Run:** A serverless platform that's easy to use and scales automatically.
-   **Google Kubernetes Engine (GKE):** A managed Kubernetes service for orchestrating complex applications.
-   **Google Compute Engine (GCE):** Provides virtual machines for maximum control.

For detailed instructions on deploying to a specific service, please refer to the official GCP documentation.

## Project Structure

-   `Dockerfile`: Defines the Docker container for the application.
-   `docker-compose.yml`: For managing the Docker container.
-   `.dockerignore`: Specifies files to be excluded from the Docker image.
-   `app/`: Main application code.
-   `app/main.py`: FastAPI application entry point.
-   `app/tests/`: Pytest tests.
-   `alembic/`: Alembic database migrations.
-   `requirements.txt`: Python dependencies.

## AI Usage & Co-Authorship
- **Claude**: Project analysis, flow design, structure generation
- **ChatGPT**: Database schema generation, field review
- **Copilot**: Test case generation, README documentation
- **Dyad**: Frontend pages with Gemini API
- **Grok**: Refactoring backend routes, services, and frontend pages

---
**AI Co-Authors:** Claude, ChatGPT, GitHub Copilot, Dyad, Gemini, Grok
