# URL Shortener

A production-inspired URL Shortener built with **FastAPI** and **PostgreSQL** to learn backend development and system design fundamentals. The project starts with a simple URL shortening service and will be incrementally enhanced with features such as caching, analytics, authentication, rate limiting, Docker, and scalable architecture.

## Project Goal

The objective of this project is to understand how a real-world backend service is designed and implemented rather than simply building a CRUD application. Throughout the project, emphasis is placed on clean architecture, separation of concerns, database design, API development, and scalability.

## Features (Version 1)

- Shorten long URLs into unique, compact links
- Redirect users to the original URL
- Store URL mappings in PostgreSQL
- Automatic database table creation using SQLAlchemy
- RESTful API built with FastAPI

## Planned Features

### Version 2
- Click analytics
- Custom short URLs
- URL expiration
- JWT Authentication
- Rate limiting
- QR code generation

### Version 3
- Redis caching
- Background workers
- Docker & Docker Compose
- Nginx reverse proxy
- Horizontal scaling
- Load balancing
- Monitoring with Prometheus and Grafana

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | FastAPI |
| Language | Python 3 |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Validation | Pydantic |
| Environment Variables | python-dotenv |
| Server | Uvicorn |

## High-Level Architecture

```text
           Client
              │
              ▼
        FastAPI Backend
              │
              ▼
        SQLAlchemy ORM
              │
              ▼
         PostgreSQL
```

## Project Structure

```text
url-shortener/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── utils.py
│
├── .env
├── requirements.txt
└── README.md
```

## Learning Objectives

This project is designed to provide hands-on experience with:

- REST API development
- Database modeling
- SQLAlchemy ORM
- Clean project architecture
- Dependency Injection
- HTTP status codes and redirects
- System Design fundamentals
- Backend scalability concepts
- Production-ready development practices

## Development Roadmap

- [x] Design system architecture
- [x] Set up FastAPI project
- [x] Configure PostgreSQL
- [x] Create SQLAlchemy models
- [ ] Build CRUD layer
- [ ] Implement URL shortening logic
- [ ] Create redirect endpoint
- [ ] Add analytics
- [ ] Integrate Redis
- [ ] Dockerize the application
- [ ] Scale to a distributed architecture

## Future Scope

As the project evolves, it will incorporate concepts commonly used in production systems, including distributed caching, asynchronous processing, load balancing, observability, and fault tolerance. The end goal is to transform a simple URL shortener into a scalable backend service that demonstrates both software engineering best practices and core system design principles.
