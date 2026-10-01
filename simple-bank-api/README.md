# Simple Bank API

FastAPI backend for the Simple Bank application. MongoDB access stays inside
repositories; controllers expose HTTP endpoints, services coordinate business
workflows, and Pydantic request models live in `schemas/`.

## Local setup

1. Copy `.env.example` to `.env` and configure MongoDB plus separate random
   values for `JWT_SECRET_KEY` (at least 32 characters) and `ADMIN_SETUP_KEY`.
2. Install `requirements.txt` in a virtual environment.
3. Run `python app.py` from this directory.
4. Open `http://127.0.0.1:5000/docs` to view the API contract.

## Layer map

- `app.py` creates the FastAPI application and shared middleware.
- `api/` composes route modules and exposes reusable authentication dependencies.
- `core/` owns application configuration, the MongoDB client, and security helpers.
- `controllers/` validates HTTP requests and maps service errors to HTTP responses.
- `services/` contains authentication, account, transaction, user, and dashboard workflows.
- `repos/` contains MongoDB reads and writes.
- `schemas/` defines request payloads.
- `tests/` covers routes, services, password handling, and authorization.

Legacy top-level `config.py`, `database.py`, and `security.py` modules re-export
the shared `core/` implementations so existing imports remain stable.

## Verification

Run `PYTHONPATH=. pytest -q` from this directory. Route/service tests use fake
repositories and do not require a running MongoDB server.