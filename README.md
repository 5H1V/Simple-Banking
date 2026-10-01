# Simple Bank Application

Full-stack project using React + Vite, FastAPI, and MongoDB Atlas. The backend uses a controller/service/repository structure.

## Backend setup

1. Open a terminal in `simple-bank-api`.
2. Create and activate a virtual environment.
3. Install dependencies: `pip install -r requirements.txt`.
4. Copy `.env.example` to `.env` and set your MongoDB Atlas URI, a random `JWT_SECRET_KEY` (at least 32 characters), and a separate `ADMIN_SETUP_KEY`. Do not commit `.env`.
5. Run `python app.py`. API docs: `http://127.0.0.1:5000/docs`.

## Frontend setup

1. Open another terminal in `simple-bank-ui`.
2. Run `npm install`.
3. Run `npm run dev`. Open `http://localhost:5173`.
4. If the API runs at a different URL, set `VITE_API_BASE_URL` to the API base ending in `/api`.

## First-time flow

1. Visit `/admin/setup` and create the administrator using `ADMIN_SETUP_KEY`. Setup can only complete once per database. After setup, remove or rotate the setup key.
2. Register a customer at `/register`, or use `/login` to sign in.
3. Customers are sent to `/dashboard`; admins are sent to `/admin/dashboard`.

## Main routes

- `/` welcome page
- `/register` customer registration
- `/login` customer/admin login
- `/admin/setup` one-time admin setup
- `/dashboard` customer-only dashboard
- `/admin/dashboard` admin-only dashboard
- `/accounts` authenticated account creation and lookup
- `/transactions` authenticated deposit and withdrawal workflow
- `/transfers` customer-only transfers between owned accounts
- `/analytics` customer-only, user-wide deposit/withdrawal analytics
- `/admin/fraud-alerts` admin-only anomaly and fraud-alert review
- `/users` admin-only user management

## Security notes

Passwords are stored as Argon2id hashes. The backend issues expiring JWTs with `CustomerToken` or `AdminToken` roles and checks permissions server-side. Customer account endpoints verify ownership; React route guards are not the security boundary. Use HTTPS outside local development. This is an educational project, not a production-ready banking platform. Account transfers use MongoDB multi-document transactions and therefore require a replica-set or sharded MongoDB deployment. Other banking operations, financial-grade money handling, idempotency, operational monitoring, and model validation need additional work before any real-world use.

## Tests

From `simple-bank-api`, run `PYTHONPATH=. pytest -q`. The tests cover API route registration, user-wide cash-flow aggregation, authentication workflows, user-service behavior, password hashing, and role/ownership checks. They do not require a running MongoDB server.
