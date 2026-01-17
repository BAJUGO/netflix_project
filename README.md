# Project DB Auth

This project is a FastAPI-based web application providing authentication and database management for a media-related database (users, authors, movies, series). It features JWT-based authentication, Redis caching, and PostgreSQL integration via SQLAlchemy.

## Overview
The application provides RESTful APIs and a frontend interface for:
- User registration and authentication (JWT).
- Managing authors, movies, and series.
- Role-based access control (Admin, Moderator, User).
- Cached data retrieval using Redis.
- Exception handling and logging.

## Stack
- **Language**: Python 3.13+
- **Framework**: FastAPI
- **Database**: PostgreSQL (Asyncpg)
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **Caching**: Redis
- **Authentication**: JWT (RS256)
- **Package Manager**: Poetry
- **Frontend**: HTML/JS/TS (served statically or via frontend server)

## Requirements
- Python 3.13 or higher
- PostgreSQL
- Redis server
- OpenSSL (to generate RSA keys for JWT)
- Node.js (for frontend dependencies in `html/` directory)

## Setup

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd project_db_auth
    ```

2.  **Install backend dependencies**:
    ```bash
    poetry install
    ```

3.  **Install frontend dependencies**:
    ```bash
    cd html
    npm install
    cd ..
    ```

4.  **Environment Variables**:
    Create a `.env` file in the root directory based on the following template:
    ```env
    DB_URL=postgresql+asyncpg://<user>:<password>@<host>:<port>/<dbname>
    ECHO=True
    JWT__PRIVATE_KEY=./certs/private.pem
    JWT__PUBLIC_KEY=./certs/public.pem
    JWT__ALGORITHM=RS256
    REDIS__HOST=localhost
    REDIS__PORT=6379
    REDIS__DB=0
    REDIS__PASSWORD=<your_redis_password>
    REDIS__USERNAME=<your_redis_username>
    ```

5.  **JWT Certificates**:
    Generate RSA keys for JWT authentication:
    ```bash
    mkdir certs
    openssl genpkey -algorithm RSA -out certs/private.pem -pkeyopt rsa_keygen_bits:2048
    openssl rsa -pubout -in certs/private.pem -out certs/public.pem
    ```

6.  **Database Migrations**:
    Apply migrations to the database:
    ```bash
    poetry run alembic upgrade head
    ```

## Run Commands

To start the FastAPI server:
```bash
poetry run uvicorn main:app --reload
```
The application will be available at `http://127.0.0.1:8000`.
Accessing the root `/` will redirect you to the interactive API documentation (`/docs`).

## Scripts
- `poetry run uvicorn main:app --reload`: Runs the development server.
- `poetry run alembic revision --autogenerate -m "description"`: Creates a new migration.
- `poetry run alembic upgrade head`: Applies migrations.

## Project Structure
```text
.
├── alembic/                # Database migration scripts
├── certs/                  # JWT RSA keys (not in version control)
├── html/                   # Frontend assets (HTML, JS, TS)
│   ├── html_pages/         # HTML templates for various views
│   ├── html_scripts/       # JavaScript/TypeScript logic
│   └── package.json        # Frontend dependencies
├── project_dir/
│   ├── authorization/      # JWT auth logic and dependencies
│   ├── core/               # Configuration and DB helper
│   ├── logging_and_exc/    # Logging and exception handlers
│   ├── models/             # SQLAlchemy models
│   ├── routers/            # FastAPI route definitions
│   └── views_part/         # CRUD logic and Pydantic schemas
├── main.py                 # Application entry point
├── pyproject.toml          # Poetry dependencies and config
└── alembic.ini             # Alembic configuration
└── TODO's                  # Project tasks and notes
```

## Environment Variables Details
- `DB_URL`: PostgreSQL connection string (must use `asyncpg`).
- `ECHO`: Boolean flag for SQLAlchemy SQL echo.
- `JWT__PRIVATE_KEY`: Path to the RSA private key file.
- `JWT__PUBLIC_KEY`: Path to the RSA public key file.
- `JWT__ALGORITHM`: JWT signing algorithm (e.g., `RS256`).
- `REDIS__HOST`: Redis server hostname.
- `REDIS__PORT`: Redis server port.
- `REDIS__DB`: Redis database index.
- `REDIS__PASSWORD`: Redis password.
- `REDIS__USERNAME`: Redis username.

## Tests
TODO: Implement backend and frontend tests. Currently, no tests are available.

## License
TODO: Add license information.
