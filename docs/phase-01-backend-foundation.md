# Phase 1: Backend Foundation

## Objective

Build the first working backend slice: a FastAPI application, environment-based
configuration, a health check endpoint, and a SQLite database connection.

This phase avoids scanning logic on purpose. A security tool should first have a
stable service boundary, clear configuration, and a place to persist results.

## What Recruiters Learn From This Phase

- You can structure a Python web API in a maintainable way.
- You understand environment variables and local development setup.
- You can connect an application to a database without hardcoding secrets.
- You know how to add a basic operational endpoint for monitoring.

## Files Created And Why

- `backend/app/main.py`: creates the FastAPI app and registers routes.
- `backend/app/core/config.py`: keeps settings in one place.
- `backend/app/database/session.py`: creates the database engine and sessions.
- `backend/app/database/models.py`: defines the first database table.
- `backend/app/api/routes/health.py`: exposes `/api/health`.
- `backend/requirements.txt`: lists Python dependencies.
- `backend/.env.example`: documents expected environment variables.
- `tests/backend/test_health.py`: proves the health endpoint works.

## Module Purpose

### `app.main`

This is the application entry point. Uvicorn imports `app.main:app`, then
FastAPI handles incoming HTTP requests.

Line-by-line notes:

- `from fastapi import FastAPI` imports the web framework class.
- `asynccontextmanager` is used for FastAPI startup and shutdown lifecycle work.
- `from backend.app.api.routes import health` imports the health route module.
- `from backend.app.core.config import settings` loads app settings.
- `from backend.app.database.session import create_database_tables` imports database initialization.
- `def create_app() -> FastAPI:` wraps app creation so tests can reuse it.
- `lifespan(...)` creates database tables before the app accepts requests.
- `app = FastAPI(...)` creates the API object and sets metadata for docs.
- `app.include_router(...)` attaches health routes under `/api`.
- `return app` gives the configured app back to the caller.
- `app = create_app()` exposes the app object Uvicorn expects.

### `app.core.config`

This module centralizes configuration.

- `BaseSettings` reads values from environment variables.
- `Settings` defines the settings the app uses.
- `app_name` and `app_version` appear in API metadata and health checks.
- `debug` controls SQL logging.
- `database_url` points to SQLite in Phase 1.
- `.env` support helps local development without changing code.
- `env_prefix="SAP_"` prevents accidental collisions with generic variables
  like `DEBUG` that may already exist on a laptop or CI runner.
- `settings = Settings()` creates one shared settings object.

Developer note: the project starts with SQLite because it is simple for a
student project and easy for reviewers to run. PostgreSQL can be introduced
later without rewriting route code.

### `app.database.models`

This module stores database table definitions.

- `Scan` represents a security scan request.
- `SQLModel, table=True` tells SQLModel to create a database table.
- `id` is the primary key.
- `target_url` stores the URL or host being assessed.
- `status` tracks scan lifecycle, such as `created`, `running`, or `completed`.
- `created_at` records when the scan was created in UTC.

### `app.database.session`

This module owns database connectivity.

- `create_engine(...)` creates the database engine.
- `echo=settings.debug` prints SQL only when debugging.
- `check_same_thread=False` is needed for SQLite with FastAPI's threaded server.
- `create_database_tables()` creates tables during local startup.
- `get_session()` is a dependency that future routes can use for database work.

### `app.api.routes.health`

This module provides a small uptime endpoint.

- `APIRouter` keeps route definitions modular.
- `@router.get("/health")` maps HTTP GET requests to `health_check`.
- The returned dictionary becomes a JSON response.

## Complete Code

The complete Phase 1 code is in the repository files listed above. Keeping the
code in real files instead of one huge tutorial block makes the project easier
to run, test, and review on GitHub.

## Interview Questions

1. Why use environment variables instead of hardcoding database URLs?
2. What is the difference between `FastAPI()` and `APIRouter()`?
3. Why does a production service need a health check endpoint?
4. What does an ORM model represent?
5. Why is UTC preferred for database timestamps?
6. What would change when moving from SQLite to PostgreSQL?

## Common Mistakes

- Putting all FastAPI routes in `main.py`.
- Committing real `.env` files with secrets.
- Using generic environment variable names that collide with system settings.
- Using local time instead of UTC for timestamps.
- Skipping tests for simple endpoints.
- Creating database sessions globally inside route functions.

## Security Considerations

- Do not store secrets in source code.
- Keep `.env.example` as documentation, not as a real secret file.
- Avoid exposing debug SQL logs in production.
- Use typed settings so unsafe configuration is easier to notice.
- Keep the health check simple and avoid leaking internal paths or stack details.

## Resume Bullet Points

- Built a FastAPI backend foundation for a web security assessment platform.
- Implemented environment-based configuration and SQLite persistence using SQLModel.
- Added a health check API and automated test coverage for service readiness.

## Expected Recruiter Impression

This phase shows that you can start a backend project cleanly, separate concerns,
and think about operational basics before adding flashy security features.

## GitHub Commit Message

```text
feat: set up FastAPI backend foundation
```
