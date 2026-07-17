# 🔗 URL Shortener

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.138-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue.svg)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-red.svg)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED.svg)](https://www.docker.com/)
[![GitHub Actions](https://img.shields.io/badge/CI-GitHub%20Actions-success.svg)](../../actions)

A **production-ready URL Shortener API** built with **FastAPI**, **PostgreSQL**, and **Redis**, following modern backend engineering practices.

The project goes beyond basic CRUD functionality by incorporating **layered architecture**, **Redis caching**, **request logging**, **global exception handling**, **background cleanup jobs**, **database versioning**, **Dockerized deployment**, and **Continuous Integration**.

Designed as a portfolio project to demonstrate how scalable backend services are structured and deployed in production environments.

---

## ✨ Highlights

- 🚀 Production-ready FastAPI backend
- 🏗️ Clean Layered Architecture (API → Service → CRUD)
- 🗄️ PostgreSQL with SQLAlchemy ORM
- ⚡ Redis caching for improved redirect performance
- 🔒 Redis-based Rate Limiting
- ⏳ URL Expiration with automatic background cleanup
- 📊 Click Analytics & Last Access Tracking
- 📦 Alembic Database Migrations
- 📝 Request Logging Middleware
- ⚠️ Centralized Global Exception Handling
- ❤️ Health & Readiness Endpoints
- 🐳 Docker & Docker Compose Support
- 🔄 GitHub Actions Continuous Integration
- 🧪 Comprehensive Test Suite using Pytest

---

## 🛠 Tech Stack

| Category | Technologies |
|----------|--------------|
| Backend | FastAPI |
| Database | PostgreSQL |
| Cache | Redis |
| ORM | SQLAlchemy |
| Database Migrations | Alembic |
| Background Jobs | APScheduler |
| Validation | Pydantic v2 |
| Testing | Pytest |
| Containerization | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| Package Manager | uv |

---

> **Goal:** Build a production-oriented backend service that demonstrates software engineering best practices, scalable architecture, and deployment workflows commonly used in modern backend development.

---

# 🏗️ System Architecture

<p align="center">
  <img src="docs/architecture.png"
       alt="URL Shortener Architecture"
       width="100%">
</p>

---

## 📦 Component Overview

| Component | Responsibility |
|-----------|----------------|
| **FastAPI Router** | Exposes REST APIs and handles HTTP requests/responses. |
| **Request Logging Middleware** | Logs every incoming request with latency and response status. |
| **Service Layer** | Implements business rules such as URL creation, expiration checks, duplicate handling, analytics, and caching strategy. |
| **CRUD Layer** | Encapsulates all database interactions using SQLAlchemy. |
| **PostgreSQL** | Persistent storage for shortened URLs and analytics. |
| **Redis** | Used for caching frequently accessed URLs and implementing request rate limiting. |
| **APScheduler** | Periodically removes expired URLs from the database without impacting request latency. |

---

# 🔄 Request Lifecycle

## URL Shortening

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Service
    participant Redis
    participant PostgreSQL

    Client->>API: POST /api/shorten
    API->>Service: Validate Request
    Service->>PostgreSQL: Check Duplicate URL / Alias
    PostgreSQL-->>Service: Result
    Service->>PostgreSQL: Store URL
    PostgreSQL-->>Service: Success
    Service-->>API: Short URL
    API-->>Client: 201 Created
```

---

## URL Redirection

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Redis
    participant PostgreSQL

    Client->>API: GET /{short_code}

    API->>Redis: Lookup Short Code

    alt Cache Hit
        Redis-->>API: Original URL
    else Cache Miss
        API->>PostgreSQL: Query URL
        PostgreSQL-->>API: Original URL
        API->>Redis: Cache Result
    end

    API-->>Client: HTTP 302 Redirect
```

---

## Background Cleanup Workflow

Expired URLs are removed automatically by a background scheduler without blocking incoming requests.

```mermaid
flowchart LR
    Scheduler["APScheduler"]
    Scheduler --> Cleanup["Cleanup Job"]
    Cleanup --> Database[(PostgreSQL)]
    Database --> Deleted["Delete Expired URLs"]
```

The scheduler runs periodically after application startup and deletes expired records based on their `expires_at` timestamp.

---

# 📂 Project Structure

The project is organized using a layered architecture that separates HTTP handling, business logic, persistence, infrastructure, and cross-cutting concerns.

```text
URL_Shortner/
│
├── .github/
│   └── workflows/           # GitHub Actions CI pipeline
│
├── alembic/                 # Database migration scripts
│
├── app/
│   ├── api/                 # FastAPI route definitions
│   ├── exceptions/          # Custom exceptions & global handlers
│   ├── middleware/          # Request logging middleware
│   ├── scheduler/           # Background cleanup jobs
│   │
│   ├── config.py           # Application configuration
│   ├── crud.py             # Database operations
│   ├── database.py         # SQLAlchemy engine & session
│   ├── dependencies.py     # Shared FastAPI dependencies
│   ├── logger.py           # Centralized logging configuration
│   ├── main.py             # Application entry point
│   ├── models.py           # SQLAlchemy models
│   ├── redis.py            # Redis client configuration
│   ├── schemas.py          # Pydantic request/response schemas
│   ├── services.py         # Business logic
│   └── utils.py            # Helper utilities
│
├── docker/
│   └── entrypoint.sh        # Container startup script
│
├── tests/                   # Unit & integration tests
│
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

---

# 🏛️ Layer Responsibilities

## API Layer

**Location:** `app/api`

The API layer is responsible only for:

- Receiving HTTP requests
- Validating inputs
- Calling the service layer
- Returning HTTP responses

Business logic is intentionally kept out of this layer.

---

## Service Layer

**Location:** `app/services.py`

The service layer contains the application's business rules.

Responsibilities include:

- URL creation
- Duplicate URL detection
- Custom alias validation
- URL expiration checks
- Redirect logic
- Analytics updates
- Cache coordination

This layer remains independent of FastAPI-specific concerns wherever possible.

---

## CRUD Layer

**Location:** `app/crud.py`

Encapsulates all database interactions using SQLAlchemy.

Examples include:

- Creating shortened URLs
- Fetching URLs by short code
- Updating analytics
- Deleting expired records

Keeping database access isolated makes it easier to modify persistence logic without affecting business rules.

---

## Infrastructure Layer

Infrastructure components provide supporting services for the application.

| Module | Responsibility |
|---------|----------------|
| `database.py` | SQLAlchemy engine & session management |
| `redis.py` | Redis client initialization |
| `logger.py` | Centralized logging configuration |
| `config.py` | Environment variable management |
| `scheduler/` | Background cleanup jobs |
| `middleware/` | Cross-cutting request logging |
| `exceptions/` | Global exception handling |

---

# 🎯 Design Principles

This project follows several backend engineering principles:

### Separation of Concerns

Each layer has a clearly defined responsibility, reducing coupling between components.

---

### Single Responsibility Principle

Every module focuses on one concern:

- Routes handle HTTP
- Services handle business logic
- CRUD handles persistence
- Middleware handles observability
- Scheduler handles background jobs

---

### Dependency Injection

FastAPI dependencies are used for shared resources such as database sessions, promoting loose coupling and easier testing.

---

### Centralized Error Handling

Domain-specific exceptions are translated into consistent HTTP responses through global exception handlers.

This avoids repetitive error handling across individual endpoints.

---

### Observability

Request logging middleware automatically captures:

- HTTP method
- Endpoint
- Status code
- Response latency

providing visibility into API behavior without modifying route implementations.

---

# 🚀 Production Engineering Features

This project was built with a focus on **production-ready backend engineering practices** rather than only implementing the core URL shortening functionality.

## 🏗️ Layered Architecture

The application follows a layered architecture:

```text
API → Service → CRUD → Database
```

Each layer has a single responsibility.

### Benefits

- Separation of concerns
- Easier testing
- Improved maintainability
- Cleaner business logic
- Independent evolution of layers

---

## ⚡ Redis Caching

Frequently accessed URLs are cached in Redis using the **Cache-Aside Pattern**.

```text
Request
   │
   ▼
Redis Cache
   │
Cache Hit?
 ├── Yes → Return URL
 └── No
        │
        ▼
 PostgreSQL
        │
        ▼
 Store in Cache
```

### Benefits

- Reduced database load
- Lower redirect latency
- Improved scalability
- Better performance for hot URLs

---

## 🚦 Redis-based Rate Limiting

The URL creation endpoint is protected using Redis-backed rate limiting.

This prevents excessive API usage while allowing legitimate traffic to continue.

### Benefits

- Protects the service from abuse
- Prevents accidental request floods
- Lightweight implementation using Redis counters

---

## ⏳ Automatic URL Expiration

URLs can optionally expire after a configurable number of days.

Expired URLs are removed automatically by a background scheduler.

### Benefits

- No manual cleanup
- Reduced database growth
- Automatic lifecycle management

---

## 🔄 Background Scheduler

The application uses **APScheduler** to execute periodic cleanup jobs.

```text
Application Startup
        │
        ▼
 APScheduler Starts
        │
        ▼
Cleanup Job Runs Periodically
        │
        ▼
Delete Expired URLs
```

### Benefits

- Keeps request latency low
- Background processing
- Easily extensible for future scheduled jobs

---

## 📝 Request Logging Middleware

Every incoming HTTP request is automatically logged.

Captured information includes:

- HTTP Method
- Request Path
- Response Status
- Processing Time

Example:

```text
INFO POST /api/shorten 201 18.42ms
INFO GET /abc123 302 3.11ms
```

### Benefits

- Better observability
- Easier debugging
- Request performance monitoring

---

## ⚠️ Global Exception Handling

The application uses centralized exception handlers instead of scattered `HTTPException` calls.

Business logic raises domain-specific exceptions:

```text
URLNotFoundException

DuplicateAliasException

URLExpiredException
```

Global handlers convert them into consistent API responses.

Example:

```json
{
  "success": false,
  "error": {
    "code": "URL_NOT_FOUND",
    "message": "Short URL does not exist."
  }
}
```

### Benefits

- Consistent API responses
- Cleaner service layer
- Easier maintenance
- Centralized error logging

---

## ❤️ Health & Readiness Probes

The application exposes health endpoints suitable for deployment environments.

| Endpoint | Purpose |
|----------|---------|
| `/health` | Verify the application is running |
| `/ready` | Verify database and Redis connectivity |

### Benefits

- Container health checks
- Deployment monitoring
- Readiness verification before serving traffic

---

## 🐳 Dockerized Deployment

The application can be started using a single command.

```bash
docker compose up --build
```

Containerization includes:

- FastAPI
- PostgreSQL
- Redis
- Alembic migrations on startup

### Benefits

- Reproducible environments
- Simple onboarding
- Production-like local development

---

## 🔄 Database Versioning with Alembic

Database schema changes are managed through Alembic migrations.

Instead of manually modifying the database, schema changes are version controlled and applied consistently.

### Benefits

- Safe schema evolution
- Reproducible deployments
- Team-friendly database changes

---

## 🧪 Automated Testing

The project includes unit and integration tests using **Pytest**.

Tests cover:

- URL shortening
- Redirects
- Duplicate aliases
- URL expiration
- Rate limiting
- Error handling

### Benefits

- Regression prevention
- Improved confidence during refactoring
- Reliable deployments

---

## ⚙️ Continuous Integration

Every push and pull request automatically triggers a GitHub Actions workflow.

The pipeline performs:

- Dependency installation
- Database initialization
- Alembic migrations
- Test execution
- Docker image build

```text
Push
 │
 ▼
Install Dependencies
 │
 ▼
Run Migrations
 │
 ▼
Run Tests
 │
 ▼
Build Docker Image
 │
 ▼
✅ Success
```

### Benefits

- Early detection of failures
- Consistent build verification
- Automated quality assurance

---

# 💡 Design Decisions

This project intentionally adopts several production-oriented design decisions to improve maintainability, scalability, and operational reliability.

---

## Why Layered Architecture?

Instead of placing all logic inside FastAPI route handlers, the application separates responsibilities into distinct layers.

```text
Client
   │
   ▼
API Layer
   │
   ▼
Service Layer
   │
   ▼
CRUD Layer
   │
   ▼
Database
```

### Why?

- Prevents business logic from leaking into API routes
- Makes services reusable
- Improves testability
- Keeps routers small and easy to understand
- Allows persistence logic to evolve independently

---

## Why PostgreSQL?

A URL shortener requires reliable persistence and transactional consistency.

PostgreSQL provides:

- ACID transactions
- Strong indexing support
- Excellent scalability
- Mature SQL ecosystem

Although NoSQL databases are often associated with URL shorteners, PostgreSQL is an excellent choice for this project's workload and demonstrates strong relational database design.

---

## Why Redis?

Redis serves two different responsibilities.

### URL Cache

Frequently accessed URLs are cached to reduce database lookups.

### Rate Limiting

Redis counters are used to implement lightweight request rate limiting.

Using Redis keeps these concerns outside the primary database, improving responsiveness while reducing database load.

---

## Why the Cache-Aside Pattern?

Instead of writing to both PostgreSQL and Redis simultaneously, the application follows the Cache-Aside Pattern.

```text
Request
   │
   ▼
Redis
   │
Cache Hit?
 ├── Yes
 │      │
 │      ▼
 │   Return
 │
 └── No
        │
        ▼
 PostgreSQL
        │
        ▼
 Store in Redis
```

### Benefits

- Simple implementation
- Better cache consistency
- Reduced database traffic
- Easy cache invalidation

---

## Why Alembic?

Schema changes are managed through version-controlled migrations instead of calling:

```python
Base.metadata.create_all()
```

Benefits include:

- Reproducible deployments
- Version-controlled database history
- Safe schema evolution
- Easier collaboration

This mirrors how production systems manage database changes.

---

## Why APScheduler?

Expired URLs should be cleaned up without affecting request latency.

Rather than deleting expired records during every redirect request, cleanup is delegated to a background scheduler.

```text
Application Startup
        │
        ▼
 APScheduler
        │
        ▼
 Periodic Cleanup
        │
        ▼
Delete Expired URLs
```

This keeps request handling fast while maintaining database hygiene.

---

## Why Request Logging Middleware?

Logging is implemented as middleware rather than inside every endpoint.

```text
Incoming Request
        │
        ▼
Logging Middleware
        │
        ▼
Business Logic
```

Advantages:

- No duplicated logging code
- Consistent request logs
- Easy performance monitoring
- Centralized observability

---

## Why Global Exception Handling?

Instead of raising `HTTPException` throughout the application, the service layer raises domain-specific exceptions.

```text
URLNotFoundException
DuplicateAliasException
URLExpiredException
```

A centralized exception handler converts these into standardized HTTP responses.

### Benefits

- Consistent error format
- Cleaner service layer
- Easier maintenance
- Improved separation of concerns

---

## Why Docker?

Containerization ensures that every environment behaves consistently.

Using Docker Compose allows the complete application stack to be started with a single command.

```bash
docker compose up --build
```

The stack includes:

- FastAPI
- PostgreSQL
- Redis

This minimizes environment-specific issues and simplifies onboarding.

---

## Why GitHub Actions?

Every push and pull request automatically validates the project by:

- Installing dependencies
- Running database migrations
- Executing the test suite
- Building the Docker image

Automating these checks helps detect regressions before code is merged.

---

## Why Health & Readiness Endpoints?

The project exposes dedicated endpoints for operational monitoring.

| Endpoint | Purpose |
|----------|---------|
| `/health` | Confirms the application is running |
| `/ready` | Verifies dependencies (PostgreSQL & Redis) are available |

These endpoints are useful for container orchestration, deployment monitoring, and load balancer health checks.

---

## Engineering Philosophy

The objective of this project was not simply to build a URL shortener.

Instead, the focus was on demonstrating how production backend services are designed by incorporating:

- Clean architecture
- Separation of concerns
- Observability
- Background processing
- Caching
- Database versioning
- Automated testing
- Continuous Integration
- Containerized deployment

The result is a backend application that emphasizes maintainability, scalability, and production readiness rather than only feature completeness.

---

# 🚀 Getting Started

## Prerequisites

Ensure the following tools are installed before running the project.

| Tool | Version |
|------|---------|
| Python | 3.12+ |
| PostgreSQL | 17+ |
| Redis | 7+ |
| Docker | Latest |
| Docker Compose | Latest |
| uv | Latest |

---

# 📥 Clone the Repository

```bash
git clone https://github.com/Rajrishi07/URL_Shortner.git

cd URL_Shortner
```

---

# ⚙️ Environment Variables

Create a `.env` file in the project root.

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/url_shortener

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

BASE_URL=http://localhost:8000

SHORT_CODE_LENGTH=6

RATE_LIMIT=5
RATE_LIMIT_WINDOW=60
```

> For Docker deployments, use the corresponding Docker service names (`postgres`, `redis`) as hosts.

---

# 💻 Local Development

Install dependencies using **uv**.

```bash
uv sync
```

Apply database migrations.

```bash
uv run alembic upgrade head
```

Start the application.

```bash
uv run uvicorn app.main:app --reload
```

The application will be available at

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

OpenAPI Specification:

```text
http://localhost:8000/openapi.json
```

---

# 🐳 Running with Docker

Build and start the complete application stack.

```bash
docker compose up --build
```

This automatically starts:

- FastAPI
- PostgreSQL
- Redis

The entrypoint script also executes:

```bash
alembic upgrade head
```

before starting the application, ensuring the database schema is always up to date.

To stop the containers:

```bash
docker compose down
```

To remove all volumes:

```bash
docker compose down -v
```

---

# 🧪 Running Tests

Execute the complete test suite.

```bash
uv run pytest
```

Run with coverage.

```bash
uv run pytest --cov=app --cov-report=term-missing
```

---

# 🔄 Database Migrations

Generate a new migration.

```bash
uv run alembic revision --autogenerate -m "migration_name"
```

Apply migrations.

```bash
uv run alembic upgrade head
```

Rollback one migration.

```bash
uv run alembic downgrade -1
```

---

# ❤️ Health Monitoring

The application exposes endpoints for deployment monitoring.

| Endpoint | Description |
|----------|-------------|
| `/health` | Application health status |
| `/ready` | Readiness check for PostgreSQL and Redis |

---

# 📖 API Overview

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/shorten` | Create a shortened URL |
| GET | `/{short_code}` | Redirect to original URL |
| GET | `/health` | Health check |
| GET | `/ready` | Readiness check |

Interactive documentation is automatically available through Swagger UI.

---

# 🔄 Continuous Integration

Every push and pull request automatically triggers the GitHub Actions workflow.

The pipeline performs:

- Install dependencies
- Start PostgreSQL
- Start Redis
- Apply Alembic migrations
- Execute Pytest
- Generate coverage report
- Verify Docker build

This ensures that every change is automatically validated before merging.

---

# 🛣️ Roadmap

The current implementation focuses on building a production-oriented backend foundation. Future improvements may include:

- [ ] User authentication & authorization
- [ ] Custom domains for shortened URLs
- [ ] QR code generation
- [ ] URL analytics dashboard
- [ ] Bulk URL shortening
- [ ] Link preview generation
- [ ] Prometheus & Grafana monitoring
- [ ] Distributed cache deployment
- [ ] Kubernetes deployment
- [ ] Distributed task processing using Celery

---

# 📚 Key Engineering Takeaways

Building this project involved much more than implementing a URL shortening algorithm. It provided practical experience with designing and engineering backend systems using production-oriented practices.

Key concepts explored include:

- Designing layered application architecture
- Separating business logic from HTTP concerns
- Managing database schema evolution with Alembic
- Applying Redis for caching and rate limiting
- Implementing centralized exception handling
- Building reusable middleware
- Scheduling background jobs using APScheduler
- Containerizing applications with Docker
- Automating testing and validation using GitHub Actions
- Writing maintainable and testable backend code

---

# 🤝 Contributing

Contributions, suggestions, and improvements are always welcome.

If you'd like to contribute:

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature/your-feature
```

3. Commit your changes

```bash
git commit -m "feat: add amazing feature"
```

4. Push the branch

```bash
git push origin feature/your-feature
```

5. Open a Pull Request

---


# 👨‍💻 Author

**Rajrishi Charan**

- GitHub: https://github.com/Rajrishi07
- LinkedIn: *(Add your LinkedIn profile here)*

---

## ⭐ If you found this project useful...

If you found this project helpful or interesting:

- ⭐ Star the repository
- 🍴 Fork the project
- 💡 Open an issue with suggestions
- 🚀 Share it with others interested in backend engineering

Every contribution and piece of feedback is greatly appreciated.