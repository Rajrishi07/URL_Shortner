# Project Context for Another LLM

## What this project is

This is a FastAPI-based URL shortener backed by PostgreSQL, with Redis used for caching and rate limiting. The repo is structured like a production-style backend rather than a toy CRUD app, and the codebase is already split into API, service, CRUD, schema, domain, and dependency layers.

## Core behavior

The app supports these main flows:

1. Create a short URL from a long URL.
2. Optionally attach a custom alias.
3. Optionally set an expiration in days.
4. Resolve a short code and redirect to the original URL.
5. Read click analytics for a short code.
6. Enforce simple IP-based rate limiting through Redis.

## Features already implemented

- URL shortening for arbitrary valid URLs.
- Redirect from short code to original URL.
- Custom aliases with collision checks.
- Expiration support with `expires_in_days`.
- Click counting and last-access tracking.
- Analytics endpoint for stored URLs.
- Redis-backed caching for resolved URLs.
- Redis-backed per-IP rate limiting.
- Test coverage for the main shortening and redirect paths.

## Main entry points

- App startup and router wiring live in [app/main.py](app/main.py).
- Shortening endpoint lives in [app/api/shorten.py](app/api/shorten.py).
- Redirect endpoint lives in [app/api/redirect.py](app/api/redirect.py).
- Analytics endpoint lives in [app/api/urls.py](app/api/urls.py).

## API surface

- `POST /api/shorten`
  - Request model: `url`, optional `custom_alias`, optional `expires_in_days`.
  - Response model: `short_url`, optional `expires_at`.
  - Duplicate aliases return `409`.
- `GET /{short_code}`
  - Redirects with `302` to the original URL.
  - Uses rate limiting via a FastAPI dependency.
  - Returns `404` when the code is missing.
  - Returns `410` when the short URL is expired.
- `GET /urls/analytics/{short_code}`
  - Returns original URL, short URL, click count, creation time, and last access time.

## Schemas

The API schemas live in [app/schemas.py](app/schemas.py).

- `URLCreate`
  - `url`: required `HttpUrl`.
  - `custom_alias`: optional string, 3 to 20 characters, only letters, numbers, `-`, and `_`.
  - `expires_in_days`: optional positive integer.
- `URLResponse`
  - `short_url`: generated short link as a string.
  - `expires_at`: optional ISO formatted datetime string.
- `URLAnalytics`
  - `original_url`: original destination.
  - `short_url`: full shortened URL.
  - `clicks`: click count.
  - `created_at`: creation timestamp.
  - `last_accessed`: last redirect timestamp or null.

## Data and persistence

- SQLAlchemy model: [app/models.py](app/models.py)
- CRUD helpers: [app/crud.py](app/crud.py)
- DB session wiring: [app/database.py](app/database.py)

The `urls` table stores:

- `id`
- `original_url`
- `short_code`
- `created_at`
- `clicks`
- `last_accessed`
- `expires_at`

Short codes are generated in [app/utils.py](app/utils.py). If a custom alias is provided, the service checks for collisions before saving.

## Service-layer logic

The core business logic is in [app/services/url_services.py](app/services/url_services.py).

- `create_short_url(...)`
  - Reuses an existing record if the same original URL already exists and no custom alias is requested.
  - Validates custom alias uniqueness.
  - Computes expiration timestamp when requested.
  - Persists the new row through the CRUD layer.
- `resolve_short_url(...)`
  - Checks Redis cache first.
  - Falls back to the database on cache miss.
  - Caches resolved URLs for one hour.
  - Rejects expired URLs with `410`.
  - Increments click count and updates last access time.

Business rules are handled mostly in the service layer, while the API layer only translates exceptions into HTTP responses.

- Duplicate custom aliases raise `ValueError` in the service and become `409` in the shorten endpoint.
- Missing short codes raise `HTTPException(404)` in the resolve path.
- Expired short codes raise `HTTPException(410)` before redirecting.
- Rate limiting raises `HTTPException(409)` when the Redis counter exceeds the configured limit.
- Validation failures for URL format, alias format, and expiration days are handled by Pydantic before the endpoint body runs.

Redis cache keys use the `url:` prefix. Rate limiting uses keys prefixed with `rate_limit:`.

## Schemas and validation

- Pydantic schemas are in [app/schemas.py](app/schemas.py).
- `URLCreate.url` is validated as an `HttpUrl`.
- `custom_alias` must match `[a-zA-Z0-9_-]+` and be 3 to 20 chars long.
- `expires_in_days` must be a positive integer when provided.

## Tests

Test setup is in [tests/conftest.py](tests/conftest.py).

Current tests cover:

- home endpoint returns `200`
- shortening a URL without expiration
- invalid URL validation
- redirect flow
- missing short code returns `404`
- custom alias creation
- duplicate alias returns `409`
- expiration handling
- invalid expiration input returns `422`

## Request flow

The practical flow for a redirect request is:

1. `app/main.py` routes `/{short_code}` to the redirect router.
2. The rate limit dependency checks Redis before the handler runs.
3. The service checks Redis cache for the short code.
4. On cache miss, it loads the row from PostgreSQL.
5. The service validates expiration, increments clicks, and updates `last_accessed`.
6. The handler returns a FastAPI `RedirectResponse` with status `302`.

For shortening requests:

1. Pydantic validates the incoming payload.
2. The service checks custom alias uniqueness or existing original URL reuse.
3. A short code is generated when needed.
4. The URL row is inserted through the CRUD helper.
5. The API returns the short URL and expiration timestamp if present.

## Environment expectations

- Python version in `pyproject.toml` is `>=3.14`.
- Dependencies include FastAPI, SQLAlchemy, Pydantic, Alembic, Redis, psycopg2-binary, pytest, httpx, python-dotenv, and uvicorn.
- Config values come from environment variables in [app/config.py](app/config.py), especially `DATABASE_URL`, `TEST_DATABASE_URL`, `BASE_URL`, `REDIS_HOST`, `REDIS_PORT`, and `REDIS_DB`.

## Important implementation notes

- The initial Alembic migration currently does not create tables; the test suite creates schema directly from SQLAlchemy metadata.
- The redirect analytics and rate limiting are Redis-aware, so running the app without Redis will affect those paths.
- There are some code-style and consistency issues in places, but the current behavior is centered around shortening, redirecting, caching, and analytics.

## Suggested mental model for changes

When modifying behavior, think in this order:

1. API layer for request/response shape.
2. Service layer for business rules.
3. CRUD layer for DB access.
4. Model/schema updates for persisted and validated data.
5. Tests for the affected flow.
