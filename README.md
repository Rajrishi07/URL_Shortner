Project: URL Shortener (Version 1)
Goal

A user submits a long URL:

https://www.youtube.com/watch?v=dQw4w9WgXcQ

We return:

http://localhost:8000/aBc123

When someone opens

http://localhost:8000/aBc123

they are redirected to the original URL.

Step 1: Requirements
Functional Requirements
Shorten a URL
Redirect to the original URL
Store URLs in a database
Non-functional Requirements
Fast lookups
Unique short codes
Simple REST API
Easy to extend later
Step 2: High-Level Design
          Client
             │
 POST /shorten
             │
             ▼
        FastAPI Server
             │
             ▼
        PostgreSQL
             │
             ▼
      URL Mapping Table

Flow:

User
 ↓
POST /shorten
 ↓
FastAPI
 ↓
Generate Short Code
 ↓
Save in PostgreSQL
 ↓
Return Short URL
Step 3: Choose the Tech Stack
Component	Technology
Backend	FastAPI
Database	PostgreSQL
ORM	SQLAlchemy
Validation	Pydantic
Server	Uvicorn

Later we'll add Redis and Docker.

Step 4: Project Structure
url-shortener/

app/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── crud.py
├── utils.py
└── config.py

requirements.txt

Each file has a single responsibility:

main.py → API routes
database.py → Database connection
models.py → Database tables
schemas.py → Request/response models
crud.py → Database operations
utils.py → Short code generation
config.py → Configuration

This separation keeps the code maintainable as the project grows.

Step 5: Database Design

We'll store one record per shortened URL.

Table: urls
Column	Type	Description
id	BIGSERIAL	Primary key
original_url	TEXT	Long URL
short_code	VARCHAR(10)	Generated code
created_at	TIMESTAMP	Creation time

Example:

id	original_url	short_code
1	https://google.com	abC123
Step 6: API Design
1. Create Short URL
POST /shorten

Request

{
    "url": "https://google.com"
}

Response

{
    "short_url": "http://localhost:8000/aBc123"
}
2. Redirect
GET /aBc123

Response

302 Redirect

The browser automatically navigates to the original URL.

Step 7: Request Flow
Client
   │
POST /shorten
   │
   ▼
Validate URL
   │
Generate Code
   │
Save to Database
   │
Return Short URL
Redirect Flow
Browser
   │
GET /aBc123
   │
Look up Database
   │
Find original URL
   │
Return HTTP 302
   │
Browser opens destination
Step 8: Database Schema
CREATE TABLE urls (
    id BIGSERIAL PRIMARY KEY,
    original_url TEXT NOT NULL,
    short_code VARCHAR(10) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
Step 9: Milestone Plan

We'll build this incrementally:

Milestone 1: Project Setup
Create the FastAPI project
Set up PostgreSQL
Configure SQLAlchemy
Verify database connectivity
Milestone 2: URL Shortening
Accept a URL
Generate a unique short code
Store it in the database
Return the shortened URL
Milestone 3: Redirection
Look up the short code
Redirect to the original URL
Return 404 for unknown codes
Milestone 4: Testing
Test API endpoints
Handle invalid URLs
Handle duplicate codes